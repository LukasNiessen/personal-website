import type { CollectionEntry } from "astro:content";
import { useMemo, useState } from "react";
import ArrowCard from "@components/ArrowCard";
import { cn } from "@lib/utils";

export type BlogPost = Pick<CollectionEntry<"blog">, "collection" | "slug" | "data">;

type Props = {
  tags: string[];
  data: BlogPost[];
};

type SortOrder = "newest" | "oldest" | "title-asc" | "title-desc";

const controlClass =
  "w-full min-h-11 rounded-lg border border-black/15 dark:border-white/20 bg-white dark:bg-neutral-950 px-3 py-2 text-sm text-black dark:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-warmAccent-secondary";

export default function Blog({ data, tags }: Props) {
  const [query, setQuery] = useState("");
  const [selectedTags, setSelectedTags] = useState(new Set<string>());
  const [year, setYear] = useState("");
  const [sort, setSort] = useState<SortOrder>("newest");
  const [tagQuery, setTagQuery] = useState("");

  const years = useMemo(
    () => [...new Set(data.map((post) => post.data.date.getUTCFullYear()))].sort((a, b) => b - a),
    [data]
  );

  // Derive results during render so the server HTML and first client render
  // contain the same complete list, without waiting for an effect.
  const posts = useMemo(() => {
    const terms = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
    const matches = data.filter((post) => {
      const postTags = post.data.tags.map((tag) => tag.toLowerCase());
      const text = [post.data.title, post.data.summary, ...postTags].join(" ").toLowerCase();

      return (
        terms.every((term) => text.includes(term)) &&
        (!year || post.data.date.getUTCFullYear().toString() === year) &&
        [...selectedTags].every((tag) => postTags.includes(tag.toLowerCase()))
      );
    });

    return matches.sort((a, b) => {
      if (sort === "title-asc" || sort === "title-desc") {
        const titleOrder = a.data.title.localeCompare(b.data.title, "en");
        return (sort === "title-asc" ? titleOrder : -titleOrder) || a.slug.localeCompare(b.slug, "en");
      }

      const dateOrder = a.data.date.getTime() - b.data.date.getTime();
      return (sort === "oldest" ? dateOrder : -dateOrder) || a.slug.localeCompare(b.slug, "en");
    });
  }, [data, query, selectedTags, sort, year]);

  const visibleTags = tags.filter((tag) => tag.toLowerCase().includes(tagQuery.trim().toLowerCase()));
  const hasFilters = Boolean(query || year || selectedTags.size || sort !== "newest");

  function toggleTag(tag: string) {
    setSelectedTags((previous) => {
      const next = new Set(previous);
      if (next.has(tag)) next.delete(tag);
      else next.add(tag);
      return next;
    });
  }

  function resetFilters() {
    setQuery("");
    setSelectedTags(new Set());
    setYear("");
    setSort("newest");
    setTagQuery("");
  }

  return (
    <div className="space-y-6">
      <section aria-label="Find articles" className="rounded-xl border border-black/10 dark:border-white/15 bg-black/[0.02] dark:bg-white/[0.03] p-4 sm:p-5">
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <label htmlFor="blog-search" className="mb-2 block text-sm font-medium text-black dark:text-white">
              Search articles
            </label>
            <input
              id="blog-search"
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search titles, summaries, and tags"
              autoComplete="off"
              className={controlClass}
              aria-controls="blog-results"
            />
          </div>
          <div>
            <label htmlFor="blog-sort" className="mb-2 block text-sm font-medium text-black dark:text-white">
              Sort by
            </label>
            <select id="blog-sort" value={sort} onChange={(event) => setSort(event.target.value as SortOrder)} className={controlClass} aria-controls="blog-results">
              <option value="newest">Newest first</option>
              <option value="oldest">Oldest first</option>
              <option value="title-asc">Title: A to Z</option>
              <option value="title-desc">Title: Z to A</option>
            </select>
          </div>
          <div>
            <label htmlFor="blog-year" className="mb-2 block text-sm font-medium text-black dark:text-white">
              Year
            </label>
            <select id="blog-year" value={year} onChange={(event) => setYear(event.target.value)} className={controlClass} aria-controls="blog-results">
              <option value="">All years</option>
              {years.map((value) => <option key={value} value={value}>{value}</option>)}
            </select>
          </div>
        </div>

        <details className="mt-4 border-t border-black/10 dark:border-white/15 pt-4">
          <summary className="cursor-pointer rounded text-sm font-medium text-black dark:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-warmAccent-secondary">
            Browse tags{selectedTags.size > 0 ? ` (${selectedTags.size} selected)` : ` (${tags.length})`}
          </summary>
          <div className="mt-4 space-y-3">
            <label htmlFor="blog-tag-search" className="sr-only">Find a tag</label>
            <input
              id="blog-tag-search"
              type="search"
              value={tagQuery}
              onChange={(event) => setTagQuery(event.target.value)}
              placeholder="Find a tag"
              autoComplete="off"
              className={controlClass}
            />
            <p id="blog-tag-help" className="text-xs text-black/60 dark:text-white/60">Articles must match all selected tags.</p>
            <div className="max-h-56 overflow-y-auto overscroll-contain p-1" role="group" aria-label="Tags" aria-describedby="blog-tag-help">
              <ul className="flex flex-wrap gap-2">
                {visibleTags.map((tag) => (
                  <li key={tag}>
                    <button
                      type="button"
                      onClick={() => toggleTag(tag)}
                      aria-pressed={selectedTags.has(tag)}
                      aria-controls="blog-results"
                      className={cn(
                        "min-h-9 rounded-full border px-3 py-1.5 text-sm transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-warmAccent-secondary",
                        selectedTags.has(tag)
                          ? "border-sky-700 bg-sky-700 text-white dark:border-sky-300 dark:bg-sky-300 dark:text-black"
                          : "border-black/15 dark:border-white/20 hover:bg-black/5 dark:hover:bg-white/10"
                      )}
                    >
                      {tag}
                    </button>
                  </li>
                ))}
              </ul>
              {visibleTags.length === 0 && <p className="py-2 text-sm">No matching tags.</p>}
            </div>
          </div>
        </details>

        {selectedTags.size > 0 && (
          <ul className="mt-4 flex flex-wrap gap-2" aria-label="Selected tags">
            {[...selectedTags].map((tag) => (
              <li key={tag}>
                <button type="button" onClick={() => toggleTag(tag)} aria-label={`Remove tag: ${tag}`} className="inline-flex min-h-9 items-center gap-2 rounded-full bg-sky-100 px-3 py-1.5 text-sm text-sky-950 dark:bg-sky-950 dark:text-sky-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-warmAccent-secondary">
                  {tag}<span aria-hidden="true">×</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <div className="flex min-h-9 items-center justify-between gap-4">
        <p role="status" aria-live="polite" aria-atomic="true" className="text-sm text-black/60 dark:text-white/60">
          {posts.length} of {data.length} articles
        </p>
        <button type="button" onClick={resetFilters} disabled={!hasFilters} className="rounded px-2 py-1 text-sm underline underline-offset-4 hover:text-black dark:hover:text-white disabled:invisible focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-warmAccent-secondary">
          Clear all
        </button>
      </div>

      <div id="blog-results">
        {posts.length > 0 ? (
          <ul className="flex flex-col gap-3">
            {posts.map((post) => <li key={post.slug}><ArrowCard entry={post} /></li>)}
          </ul>
        ) : (
          <div className="rounded-xl border border-dashed border-black/20 dark:border-white/20 px-5 py-12 text-center">
            <h2 className="text-lg font-semibold text-black dark:text-white">No articles found</h2>
            <p className="mt-2 text-sm">Try another search or remove a tag or year filter.</p>
            <button type="button" onClick={resetFilters} className="mt-4 rounded px-3 py-2 text-sm font-medium underline underline-offset-4 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-warmAccent-secondary">Reset filters</button>
          </div>
        )}
      </div>
    </div>
  );
}
