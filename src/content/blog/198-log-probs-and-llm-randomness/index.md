---
title: "LLMs Are Not Actually Probabilistic"
summary: "The neural network does deterministic calculations. The results describe probabilities. A walkthrough from chat messages and billions of weights to logits, sampling, and invisible watermarks."
date: "Nov 7 2026"
tags:
  - AI
  - LLM
  - Machine Learning
  - Privacy
  - Watermarking
---

# LLMs Are Not Actually Probabilistic

You often hear that traditional software is deterministic, while LLMs are probabilistic. And the way this is used makes it sound as if something random happens inside the neural network, some unpredictable magic.

That's not how it works.

I'm talking about running an already trained model here. The weights are there. We give it an input, run a huge amount of calculations, and get scores for the possible next tokens. **That computation is deterministic, from its input all the way to its output.** The scores let us calculate probabilities. They don't make the calculation itself random.

(Yes, the technical term *probabilistic model* is correct: the model represents probabilities)

What we then do with these probabilities is a separate decision. We can always take the highest-scoring next token. Or we can sample, meaning we randomly choose a token according to the probabilities. In the standard generation process, that is where the random choice comes in. After the neural network has calculated its result for that step.

So let me first make the argument without going into neural networks. Then we'll follow a chat message through the calculations, and finally look at log probs and what we can do with them.

## Calculating a Probability Is Not a Random Operation

Suppose we have a bag with 70 red balls and 30 blue balls. We want the probability of getting red when drawing one ball uniformly at random. A program calculates:

```text
70 / (70 + 30) = 0.70
```

This is obviously deterministic. Run it once or a million times, the calculation gives us 70%. We haven't even drawn a ball yet!

Now we can simulate a draw using a random number. Fine. But that is another operation. The calculation was already finished.

The same distinction applies to an LLM. Calculating the probabilities is one thing. Choosing a token from them is another. We should not mix these up just because both are usually wrapped into one API call.

And weighted random selection is completely normal software. A game can give you a common item with 70% probability and a rare item with 30%. No neural network needed. Shannon already described generating text from letter and word probabilities in [1948](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x). Metropolis and Ulam described using random samples to simulate physical processes in their [1949 Monte Carlo paper](https://doi.org/10.1080/01621459.1949.10483310).

So the random selection at the end of a prediction step is nothing new. And it doesn't explain what makes an LLM useful. The interesting part is what the model calculates for an enormous range of inputs. That is difficult and is entirely deterministic.

## What Happens Between Your Message and the Logits

Okay, let's follow one request through the model.

### First We Assemble the Input

You type: "Will it rain tomorrow?"

That message alone is usually not the input. The application might also provide a system prompt, your conversation history, tool descriptions, retrieved documents, and previous tool results. For a text model, these are formatted into one sequence using the model's **chat template**. Special markers tell it where messages start and stop and which role each message has.

A simplified version could look like this:

```text
[SYSTEM] You are a helpful travel assistant.
[TOOLS] lookup_weather(city): get the weather forecast for a city.
[USER] I'm planning a trip to Berlin.
[ASSISTANT] What would you like to know?
[USER] Will it rain tomorrow?
[ASSISTANT]
```

These are illustrative markers, not a particular API format. The point is that your message, the instructions, and the previous conversation all become part of the input. "Context" is not some separate magical thing outside the calculation. [Hugging Face's chat template documentation](https://huggingface.co/docs/transformers/chat_templating) shows how this formatting works.

Tool descriptions work similarly: the model receives information about the available tools and their arguments. It can then generate a tool call. The application executes that call and supplies the result as more input; the neural network doesn't itself make an HTTP request to a weather service. [The tool-use documentation](https://huggingface.co/docs/transformers/chat_extras) walks through this process.

### Then Text Becomes Numbers

The tokenizer splits the input into **tokens**: words, parts of words, punctuation, and special markers. Each token has an integer ID.

An ID by itself doesn't tell us much. So the model looks it up in a learned **embedding table**, which gives us a vector of numbers. Think of a vector here simply as a list. Each token becomes a list of, for example, 8,192 numbers.

If our input has 1,000 tokens, we now have 1,000 such lists. Put them together and we have a `1,000 × 8,192` matrix. The model also incorporates information about positions, so word order affects the calculation.

Those numbers are then transformed as they move through the network. We keep the model's learned weights fixed, but the values calculated for this particular input change from layer to layer.

### What the Matrix Calculations Actually Do

Most of those weights are organized into matrices. Multiplying an input vector by a weight matrix produces another vector. Each output value is a weighted sum of input values.

Here's a tiny example:

```text
Input:   [2, -1]

Weights: [3,  4]
         [1, -2]

First output:  3 × 2 + 4 × (-1)    = 2
Second output: 1 × 2 + (-2) × (-1) = 4

Output:  [2, 4]
```

Four multiplications and two additions. Nothing random. Different weights would give us a different function. Different input numbers could give us a different result. But with these weights and this input, the result is determined.

Now make the vectors thousands of numbers long and the matrices thousands of rows and columns wide. Apply these calculations repeatedly. That's the scale we're dealing with.

There is more than multiplication, of course. **Activation functions** transform the numbers nonlinearly, so the network can represent relationships that linear calculations alone couldn't. For example, SiLU calculates `x / (1 + exp(-x))`. Put in `2` and you get approximately `1.7616`. Again, a fixed calculation. This function is part of Llama's gated feed-forward block, described in [the Llama 3 paper](https://arxiv.org/html/2407.21783v3#S3.T3).

**Attention** lets a token's representation incorporate information from the current and earlier permitted positions. The model calculates matching scores, turns those into weights, and uses them to mix information. This is how the representation can depend on the surrounding context. These attention weights are calculated too; the model doesn't randomly pick which earlier words to look at. Add normalization and connections that carry earlier values forward, and we have the main ingredients of a transformer block. [Attention Is All You Need](https://arxiv.org/html/1706.03762v7) introduced this design.

Then we do this through many blocks. The output of one becomes the input to the next.

### How Much Calculation Are We Talking About

Let's use an actual model for scale. Meta's **Llama 3.3 70B** has roughly 70 billion parameters, meaning learned numbers, mostly entries in weight matrices. Its vectors are 8,192 numbers wide and pass through 80 transformer blocks. See [Meta's model definitions](https://github.com/meta-llama/llama-models/blob/main/models/sku_list.py).

One `8,192 × 8,192` matrix applied to one vector already takes **67,108,864 multiplications**, plus roughly as many additions. That's about **134 million arithmetic operations** for one matrix application. A multiplication and an addition count as two floating-point operations, or **FLOPs**, even if the hardware performs them in one fused instruction. [NVIDIA's matrix guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html) explains this counting convention.

For a rough estimate of the main matrix work in a dense 70-billion-parameter model, think around **70 billion multiplications plus 70 billion additions per token**, or roughly **140 billion FLOPs**. Here, dense means we use the main weight matrices for every token. Generating about 500 tokens puts that estimate at **70 trillion operations**.

This estimate leaves out processing the original prompt and extra work such as attention over the context. Also, **mixture-of-experts** models only use some of their weights for each token. [DeepSeek-V3](https://arxiv.org/html/2412.19437v2), for example, reports 671 billion total parameters but 37 billion activated per token. So you can't just multiply every model's total parameter count by two.

So yes, even producing a normal answer can involve trillions of operations. This is why GPUs and other AI accelerators matter. They perform many operations in parallel, with specialized units such as Tensor Cores accelerating matrix multiply-and-add work. CPUs can run these models too, but large models at useful serving speeds need substantial compute and memory bandwidth. [NVIDIA's GPU architecture guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html) explains the hardware side.

We also avoid repeating unnecessary work. The initial prompt is processed largely in parallel, and a **KV cache** stores attention keys and values from previous tokens for reuse. Even with this caching, moving weights and cached values through memory can be the bottleneck when generating a few responses at a time. [NVIDIA's inference guide](https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/) explains these optimizations.

### Finally We Get the Logits

After the transformer blocks, a final learned matrix maps the representation at the last position to a score for each token in the vocabulary. These scores are the **logits**. In our Llama example, that's 128,256 possible tokens, so 128,256 scores.

That's it. The network has done its work **for this next-token prediction**.

```text
Messages, instructions, tools, context
                    ↓
       Formatted sequence of token IDs
                    ↓
          Vectors of learned numbers
                    ↓
   Many layers of matrix calculations,
   attention and nonlinear transformations
                    ↓
          One score per possible token
                    ↓
                 Logits
```

All of this is specified mathematics. The fixed weights and input determine the result. Being too complicated for us to calculate in our heads does not make it random.

The weights themselves came from training. Backpropagation calculates how changing weights would change the loss, and an optimizer updates them. In next-token pretraining, that loss rewards assigning more probability to the observed next tokens. Initialization and training can involve randomness, but we don't randomly initialize the model again for every chat message. The trained weights are already there. Backpropagation itself is also much older than LLMs; see [Rumelhart, Hinton, and Williams in 1986](https://www.nature.com/articles/323533a0).

This entire process, of training the weights, and then performing these calculations, this is the magic. And all of it is deterministic and fully predictable.

One practical note: deterministic mathematics doesn't automatically guarantee bit-for-bit repeatability from every hosted service. Parallel floating-point arithmetic can produce small numerical differences, and a small difference can change which of two nearly tied tokens wins. A service can also change the input or model version. These are concrete implementation issues, described in [PyTorch's reproducibility guidance](https://docs.pytorch.org/docs/stable/notes/randomness.html). They don't follow from the fact that the model's predictions are probabilities.

## What We Do With the Scores

Okay, the network has produced its scores. The learned computation for this prediction is done. Now we need to turn the result into an actual answer.

This next part is still important in AI engineering. A model can be good and the application can still use it badly. So let's look at log probs and token selection, which libraries often bundle with the model into one call.

### From Logits to Probabilities

Logits are raw scores. They can be positive or negative and don't need to add up to anything. **Softmax** converts them into probabilities that add up to one:

```text
probability_i = exp(score_i) / sum(exp(score_j) for every candidate j)
```

We exponentiate each score and divide by the total. A bigger score gives a bigger probability. [Google's softmax explanation](https://developers.google.com/machine-learning/recommendation/dnn/softmax) shows the conversion.

Suppose the input ends with "The cat sat on the". For a small example, pretend there are only four possible next tokens, each a whole word:

| Next token | Probability | Natural log probability |
| --- | ---: | ---: |
| `mat` | 60% | -0.5108 |
| `sofa` | 25% | -1.3863 |
| `floor` | 10% | -2.3026 |
| `rug` | 5% | -2.9957 |

These numbers are made up, but the calculation is real. The model didn't roll a die to give `mat` 60%. We calculated that probability from its scores.

### Why We Use Log Probs

A **log prob** is simply the logarithm of a probability. Using the natural logarithm:

```text
logprob = ln(probability)
probability = exp(logprob)
```

So `ln(0.60)` is approximately `-0.5108`. Closer to zero means more likely. A probability of one has log prob zero; probabilities approaching zero have increasingly negative log probs.

Why bother? Because the probability assigned to a sequence is the product of its token probabilities. Suppose three successive tokens have conditional probabilities `0.6`, `0.5`, and `0.2`:

```text
0.6 × 0.5 × 0.2 = 0.06
```

Each probability is calculated with the preceding tokens as context. We are not assuming that the tokens are independent.

For a long sequence, multiplying tiny numbers can make the result too small for the computer to represent. It rounds to zero. This is called **underflow**, and obviously zero is not useful if we wanted to compare two small probabilities.

Logarithms turn multiplication into addition:

```text
ln(0.6) + ln(0.5) + ln(0.2) = ln(0.06) ≈ -2.8134
```

So we can add log probs instead. Implementations use a stable **log-softmax** calculation to obtain them directly from logits, avoiding the detour through tiny probabilities.

Note that log probs aren't a mandatory stop before selecting a token. They are a useful representation for scoring and inspecting results.

### Now We Choose a Token

We have two straightforward options:

- **Greedy decoding:** take the highest-scoring token. In our example, `mat`.
- **Sampling:** make a weighted random choice. Here `mat` has a 60% chance, `sofa` 25%, and so on.

Same model, same scores, different selection rule. [Hugging Face's generation guide](https://huggingface.co/docs/transformers/generation_strategies) describes both.

Greedy decoding can even select the highest logit directly. Softmax and logarithms preserve the ordering, so we don't need them just to find the maximum.

Once we've chosen a token, it becomes part of the context for the next prediction. We repeat until the response ends. This is why "after the model" means **after each prediction step**, not after an entire answer has already appeared.

The random number generator used for sampling is generally pseudorandom too. Fix its state and the rest of the computation, and a sampled run can be reproducible. But for our argument, the important point is simpler: we can leave the random draw out entirely.

### Temperature Changes the Distribution

For positive temperature `T`, we apply softmax to `logits / T`. Lower temperatures concentrate probability on the stronger candidates. Higher temperatures make the alternatives more competitive.

Using our example as the distribution at temperature one:

| Token | Temperature 0.5 | Temperature 1 | Temperature 2 |
| --- | ---: | ---: | ---: |
| `mat` | 82.76% | 60% | 42.69% |
| `sofa` | 14.37% | 25% | 27.56% |
| `floor` | 2.30% | 10% | 17.43% |
| `rug` | 0.57% | 5% | 12.32% |

You can calculate the `0.5` column by squaring the original probabilities and normalizing them again. For temperature `2`, take square roots and normalize. This assumes no additional token filtering.

Again, the temperature calculation is deterministic. We change the distribution, then use it to choose a token.

In systems that support it, **temperature zero usually requests greedy selection**. It's a special case, not literal division by zero. With fixed scores and a fixed rule for ties, there is no random draw. With a deterministic implementation, the full generation loop can be deterministic too.

Of course this doesn't make the answer correct. Greedy decoding picks the best-scoring next token. It doesn't guarantee the best complete answer. Sampling can provide useful variety and alternative solution attempts. So the selection strategy matters, even though it isn't where the model's learned capabilities come from.

### What Log Probs Tell Us

Suppose the two strongest candidates have probabilities `0.31` and `0.30`. Greedy decoding picks the first. It would also pick the first if the probabilities were `0.99` and `0.001`. But those are very different predictions! Log probs let us inspect that difference instead of only seeing the selected token.

We can also score proposed continuations by adding their conditional log probs, without sampling anything. For different lengths, be careful: every additional token contributes a nonpositive log prob, so raw scores have a length bias.

Very important: a high token probability is **not a truth guarantee**. A familiar false statement can receive high probability. Several correct phrasings can divide probability among them. These numbers describe the model's predictions of tokens in context, not the probability that its whole answer is factually correct.

And when inspecting log probs, check which distribution you're looking at: the original model distribution or one adjusted by temperature and filtering. Changing sampling settings doesn't mean the model has learned something new.

## Watermarking and Signals You Cannot See

Now here's something interesting we can do with these choices. Suppose several words would fit well. We can influence which one gets picked and, over a whole answer, leave a detectable pattern. The sentences still look completely normal.

### How Text Watermarking Uses Token Choices

A classic example is the approach proposed by Kirchenbauer and colleagues in **2023**. At each step, a pseudorandom procedure marks some candidate tokens as a favored group, often called the **green list**. The generator gives these tokens a modest probability boost. Across enough text, the result contains more favored choices than expected by chance. A detector can test for that pattern. [A Watermark for Large Language Models](https://arxiv.org/abs/2301.10226) describes the method.

The signal is in the pattern of ordinary token choices. You don't need invisible Unicode characters or a hidden footer.

Anthropic already does this. As of November 2026, **supported Claude models generate watermarked text**. Which models and platforms are covered is documented in [Anthropic's watermark documentation](https://platform.claude.com/docs/en/build-with-claude/text-watermark).

Claude uses a version of Google DeepMind's **SynthID-Text**, rather than the exact green-list method above. At a high level, a key and preceding text guide the pseudorandom choices, producing a pattern that can later be tested. Anthropic says the watermark contains **no information identifying a person, organization, or chat**. Its purpose is to assess whether Claude likely contributed to the text. [Anthropic's explanation](https://www.anthropic.com/news/claude-text-watermark) is explicit about this distinction.

These mechanisms operate in the generation pipeline. Google's [SynthID documentation](https://ai.google.dev/responsible/docs/safeguards/synthid) describes its implementation as a processor that modifies token scores using pseudorandom values. The ordinary model calculations still supply the underlying candidates.

Detection is statistical. Short passages, tightly constrained answers, and heavily edited text can provide too little surviving signal. A detector also has false-positive and false-negative tradeoffs. A missing watermark therefore does not prove that a human wrote the text.

### Watermarks Can Also Help Trace a Copy

There is a privacy issue here too. Give every recipient a differently watermarked copy, and a copy published later may tell you which delivery it came from. The person sharing it might have no idea that identifier is there.

This can help find a leak. It can also help trace someone who thought they were sharing anonymous content. But the design matters: a mark that says "probably generated by Claude" does not tell you which person used Claude. You need different marks and a way to connect them to recipients for that.

And the mark doesn't send data anywhere. Someone has to obtain the content and know how to detect and interpret it. The concerning part is that you can share something without realizing how much it reveals.

This is not unique to AI.

### Printers Can Mark Physical Paper

Some color laser printers place tiny yellow dots on printed pages. EFF reverse-engineered a Xerox DocuColor pattern that encoded the printer's serial number and the printing date and time. The dots are difficult to see under ordinary lighting but can be examined with magnification or blue light. [EFF's decoding guide](https://w2.eff.org/Privacy/printers/docucolor/) documents the actual pattern.

So you can hold a printed page in your hand, read every word, and still miss information identifying the printer and when it was used. Connecting that printer to a particular person takes more evidence, of course.

### Cameras Can Leave a Hardware Fingerprint

With cameras, something similar can happen for a different reason.

Tiny manufacturing differences between sensor pixels produce a characteristic noise pattern called **photo-response non-uniformity**, or **PRNU**. Forensic analysis can compare that pattern with reference images to help associate a photograph with a particular camera. A [Purdue study published in the FBI's Forensic Science Communications](https://archives.fbi.gov/archives/about-us/lab/forensic-science-communications/fsc/jan2009/research) tested this approach.

So we don't need to assume that someone secretly put your name or a device ID into the pixels. The sensor itself can leave a fingerprint. Whether it can actually be matched depends on the image processing and the reference images available.

Phone photos can also contain location metadata, which is a separate mechanism. GPS coordinates in file metadata are not a secret pattern in the pixels. [Apple's photo privacy guidance](https://support.apple.com/en-ie/guide/personal-safety/ips0d7a5df82/web) explains how location information can accompany shared photos.

### Audio Can Identify an Individual Copy

Music distribution provides a more direct example of identifying a recipient. A distributor can give each recipient a promotional audio file containing a different inaudible watermark. If a copy later appears elsewhere, the mark can be matched to the original delivery.

[MusicTrace describes this workflow](https://musictrace.de/index.php/audio-watermarking-en): the identifier is embedded in the audio signal itself, rather than merely stored in an editable metadata tag. Finding that copy establishes a connection to a delivery; it does not automatically prove that the recipient personally leaked it.

Audio watermarks also support audience measurement. [Nielsen has documented embedding inaudible identifiers in broadcast audio](https://www.nielsen.com/news-center/2019/successful-transmission-of-next-gen-tv-standard-audience-measurement-technology-completed/) so measurement equipment can recognize the programming. Here the signal identifies content, while separate equipment performs the measurement.

So you can read every word of a text, inspect a printed page, or listen carefully to a song and still miss information carried by it. Someone with the right tools may see something you don't.

With LLM text, ordinary choices between plausible next tokens are enough to create such a signal. The model has calculated the options. We decide how to use them. And that decision can do quite a bit more than pick the next word.
