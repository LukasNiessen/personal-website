import { formatDate } from "@lib/utils";
import type { CollectionEntry } from "astro:content";

type Props = {
  entry: Pick<CollectionEntry<"blog"> | CollectionEntry<"projects">, "collection" | "slug" | "data">;
  pill?: boolean;
};

export default function ArrowCard({ entry, pill }: Props) {
  return (
    <a
      href={`/${entry.collection}/${entry.slug}`}
      className="group p-5 gap-3 flex items-center border rounded-xl hover:bg-black/[0.025] dark:hover:bg-white/5 hover:border-warmAccent-secondary/60 focus-visible:border-warmAccent-secondary focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-warmAccent-secondary motion-safe:hover:-translate-y-0.5 motion-safe:focus-visible:-translate-y-0.5 hover:shadow-sm border-black/15 dark:border-white/20 transition-all duration-200 ease-out motion-reduce:transition-none"
    >
      <div className="w-full min-w-0 group-hover:text-black group-hover:dark:text-white blend">
        <div className="flex flex-wrap items-center gap-2">
          {pill && (
            <div className="text-sm capitalize px-2 py-0.5 rounded-full border border-black/15 dark:border-white/25">
              {entry.collection === "blog" ? "post" : "project"}
            </div>
          )}
          <div className="text-sm text-black/60 dark:text-white/60">
            {formatDate(entry.data.date)}
          </div>
        </div>
        <div className="font-semibold mt-3 text-black dark:text-white text-lg md:text-xl">
          {entry.data.title}
        </div>

        <div className="text-sm mt-2 line-clamp-2">{entry.data.summary}</div>

        <ul className="flex flex-wrap mt-5 gap-1">
          {entry.data.tags.map((tag: string) => (
            <li
              key={tag}
              className="text-xs py-0.5 px-1 rounded bg-black/5 dark:bg-white/10 text-black/60 dark:text-white/60"
            >
              {tag}
            </li>
          ))}
        </ul>
      </div>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
        className="shrink-0 stroke-current group-hover:stroke-black group-hover:dark:stroke-white"
      >
        <line
          x1="5"
          y1="12"
          x2="19"
          y2="12"
          className="scale-x-0 group-hover:scale-x-100 group-focus-visible:scale-x-100 translate-x-4 group-hover:translate-x-1 group-focus-visible:translate-x-1 transition-all duration-200 ease-out motion-reduce:transition-none"
        />
        <polyline
          points="12 5 19 12 12 19"
          className="translate-x-0 group-hover:translate-x-1 group-focus-visible:translate-x-1 transition-all duration-200 ease-out motion-reduce:transition-none"
        />
      </svg>
    </a>
  );
}
