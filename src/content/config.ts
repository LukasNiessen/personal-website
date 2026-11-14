import { defineCollection, z } from 'astro:content';

// Front matter contains calendar dates, including legacy English month names.
// Parse them in UTC so server and browser time zones cannot change the day.
const calendarDate = z.preprocess((value) => {
	if (typeof value === 'string' && (
		/^[A-Za-z]+\s+\d{1,2},?\s+\d{4}$/.test(value) ||
		/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(value)
	)) {
		return `${value} UTC`;
	}
	return value;
}, z.coerce.date());

const work = defineCollection({
	type: 'content',
	schema: z.object({
		company: z.string(),
		role: z.string(),
		dateStart: calendarDate,
		dateEnd: z.union([calendarDate, z.string()]),
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
		date: calendarDate,
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
		date: calendarDate,
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
		date: calendarDate,
	}),
});

export const collections = { work, blog, projects, legal };
