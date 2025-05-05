# Personal Blog

This is my personal homepage and blog. I built this site with Astro, Tailwind CSS, TypeScript, and a dash of React for the interactive bits. The website is in **beta**.

Feel free to use it however you like, privately or commercially.

## 🚀 Built For Performance and SEO

Everything is static.

- Pages weigh in under 100kb
- Renders in about 40ms locally

## 🛠️ Dev Commands

Got the code? Here's how to play with it:

| Command           | What It Does                               |
| ----------------- | ------------------------------------------ |
| `npm i`           | Gets all the goodies installed             |
| `npm run dev`     | Fires up local dev at `localhost:4321`     |
| `npm run build`   | Creates production-ready site in `./dist/` |
| `npm run preview` | Checks out your build before it goes live  |

## Architecture

I used Astro and React. The site therefore consists of static files. They are hosted on AWS S3. Additionally, I use CloudFront and Route 53.

## Contributing

You are very welcome to contribute! I use GitHub Flow, so if you want to contribute, just create a feature/fix branch and create a PR when ready. As soon as it's merged, it will be automatically deployed.

Note that you can reuse this project however you like, including creating your own blog from it by just replacing texts and images. 😊

## Todo

- Proper CI, that is especially linting

## 📜 License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
