import { defineCollection, z } from 'astro:content';

const work = defineCollection({
	type: 'content',
	schema: z.object({
		company: z.string(),
		role: z.string(),
		dateStart: z.coerce.date(),
		dateEnd: z.union([z.coerce.date(), z.string()]),
		location: z.string().optional(),
		employmentType: z.string().optional(),
		workMode: z.string().optional(),
	}),
});

const blog = defineCollection({
	type: 'content',
	schema: z.object({
		title: z.string(),
		summary: z.string(),
		date: z.coerce.date(),
		tags: z.array(z.string()),
		draft: z.boolean().optional(),
		repoUrl: z.string().optional(),
		xLink: z.string().optional(),
		linkedInLink: z.string().optional(),
	}),
});

const projects = defineCollection({
	type: 'content',
	schema: z.object({
		title: z.string(),
		summary: z.string(),
		date: z.coerce.date(),
		tags: z.array(z.string()),
		draft: z.boolean().optional(),
		demoUrl: z.string().optional(),
		repoUrl: z.string().optional(),
	}),
});

const legal = defineCollection({
	type: 'content',
	schema: z.object({
		title: z.string(),
		date: z.coerce.date(),
	}),
});

export const collections = { work, blog, projects, legal };
