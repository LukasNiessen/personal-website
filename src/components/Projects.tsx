import type { CollectionEntry } from "astro:content";
import { useState, useEffect } from "react";
import ArrowCard from "@components/ArrowCard";
import { cn } from "@lib/utils";

type Props = {
  tags: string[];
  data: CollectionEntry<"projects">[];
};

export default function Projects({ data, tags }: Props) {
  const [filter, setFilter] = useState(new Set<string>());
  const [projects, setProjects] = useState<CollectionEntry<"projects">[]>([]);

  useEffect(() => {
    setProjects(
      data.filter((entry) =>
        Array.from(filter).every((value) =>
          entry.data.tags.some(
            (tag: string) => tag.toLowerCase() === String(value).toLowerCase()
          )
        )
      )
    );
  }, [filter, data]);

  function toggleTag(tag: string) {
    setFilter(
      (prev) =>
        new Set(
          prev.has(tag) ? [...prev].filter((t) => t !== tag) : [...prev, tag]
        )
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
      <div className="col-span-3 sm:col-span-1">
        <div className="sticky top-24">
          <div className="text-sm font-semibold uppercase mb-2 text-black dark:text-white">
            Filter
          </div>
          <ul className="flex flex-wrap sm:flex-col gap-1.5">
            {tags.map((tag) => (
              <li key={tag}>
                <button
                  onClick={() => toggleTag(tag)}
                  className={cn(
                    "w-full px-2 py-1 rounded",
                    "whitespace-nowrap overflow-hidden overflow-ellipsis",
                    "flex gap-2 items-center",
                    "bg-black/5 dark:bg-white/10",
                    "hover:bg-black/10 hover:dark:bg-white/15",
                    "transition-colors duration-300 ease-in-out",
                    filter.has(tag) && "text-black dark:text-white"
                  )}
                >
                  <svg
                    className={cn(
                      "size-5 fill-black/50 dark:fill-white/50",
                      "transition-colors duration-300 ease-in-out",
                      filter.has(tag) && "fill-black dark:fill-white"
                    )}
                  >
                    <use
                      href={`/ui.svg#square`}
                      className={cn(!filter.has(tag) ? "block" : "hidden")}
                    />
                    <use
                      href={`/ui.svg#square-check`}
                      className={cn(filter.has(tag) ? "block" : "hidden")}
                    />
                  </svg>
                  {tag}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="col-span-3 sm:col-span-2">
        <div className="flex flex-col">
          <div className="text-sm uppercase mb-2">
            SHOWING {projects.length} OF {data.length} PROJECTS
          </div>
          <ul className="flex flex-col gap-3">
            {projects.map((project) => (
              <li key={project.slug}>
                <ArrowCard entry={project} />
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
