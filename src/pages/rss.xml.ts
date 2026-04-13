import rss from "@astrojs/rss"
import { getCollection } from "astro:content"
import { SITE } from "@consts"

type Context = {
  site: string
}

export async function GET(context: Context) {
	const posts = await getCollection("blog")
  const projects = await getCollection("projects")

  const blogItems = posts.map((item) => ({ ...item, collection: "blog" as const }))
  const projectItems = projects.map((item) => ({ ...item, collection: "projects" as const }))

  const items = [...blogItems, ...projectItems]

  items.sort((a, b) => new Date(b.data.date).getTime() - new Date(a.data.date).getTime())

  return rss({
    title: SITE.TITLE,
    description: SITE.DESCRIPTION,
    site: context.site,
    items: items.map((item) => ({
      title: item.data.title,
      description: item.data.summary,
      pubDate: item.data.date,
      link: item.collection === "blog"
        ? `/blog/${item.slug}/`
        : `/projects/${item.slug}/`,
    })),
  })
}
