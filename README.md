# Personal Blog

This is my personal homepage and blog. I built this site with Astro, Tailwind CSS, TypeScript, and a dash of React for the interactive bits. The website is in **beta**. Link: https://lukasniessen.com

Feel free to use this repo however you like, privately or commercially.

![Screenshot homepage](screenshot_homepage.png?raw=true "Screenshot")

## 🚀 Built For Performance and SEO

Everything is static.

- Pages weigh in under 100kb
- Renders in about 40ms locally

## 🛠️ Dev Commands

| Command           | What It Does                               |
| ----------------- | ------------------------------------------ |
| `npm i`           | Gets all the goodies installed             |
| `npm run dev`     | Fires up local dev at `localhost:4321`     |
| `npm run build`   | Creates production-ready site in `./dist/` |
| `npm run preview` | Checks out your build before it goes live  |

## Architecture

I used Astro and React. The site therefore consists of static files. They are hosted on AWS (S3 as a server for static web sites plus CloudFront).

This project is push-based GitOps.

You can find the infrastructure under `\infrastructure`. It uses Terraform.

## Contributing

You are very welcome to contribute! I use GitHub Flow, so if you want to contribute, just create a feature/fix branch and create a PR when ready. As soon as it's merged, it will be automatically deployed.

Note that you can reuse this project however you like, including creating your own blog from it by just replacing texts and images. 😊

## TODO

- Add linting
- Add prettier or similar (should be auto applied in IDE as well)
- Mobile first!
- Blog part: categories needs UX/UI redoing, posts should rather be in cards, two per row, instead of one "big card" per row
- Remove images from articles as assets. Upload to a CDN for example and replace by links. The website's size will grow else, bad for SEO

## 📜 License

This project is under the MIT License
