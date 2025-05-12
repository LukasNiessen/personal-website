import type { Dictionary, Links, Page, Site, Socials } from "@types";

// Dictionaries
export const DICT_EN: Dictionary = {
  // Global
  "site.title": "Lukas Niessen",
  "site.description": "Software Architect and Full Stack Developer",
  "site.author": "Lukas Niessen",

  // Pages
  "work.title": "Resume",
  "work.description": "Places I have worked.",
  "blog.title": "Blog",
  "blog.description": "Writing on topics I am passionate about.",
  "projects.title": "Projects",
  "projects.description": "Recent projects I have worked on.",
  "search.title": "Search",
  "search.description": "Search all posts and projects by keyword.",

  // Work page
  "work.mode.remote": "Remote",
  "work.mode.hybrid": "Hybrid",
  "work.mode.on-site": "On-site",
  "work.employmentType.full-time": "Full-time",
  "work.employmentType.part-time": "Part-time",
  "work.employmentType.contract": "Contract",
  "work.employmentType.freelance": "Freelance",

  // Home page
  "home.subtitle": "Software Architect & Full Stack Developer",
  "home.about":
    "I'm a Software Architect & Full Stack Developer with 7 years of experience, spanning startups, consulting and corporations. I led a frontend team and software architecture at SocialHubs. My tech stack includes: Azure, Google Cloud Platform, JavaScript, TypeScript, Angular, React, Java, Microservices, and MicroFrontends. I love writing and sharing knowledge... 😊",
  "home.interests":
    "I love web, cloud, mathematics, piano, caffeine. Let's get in touch!",
  "home.education": "BSc in Mathematics at University of Bonn",
  "home.connect": "Getting in touch",
  "home.recent.projects": "Recent projects",
  "home.all.projects": "All projects",
  "home.recent.posts": "Recent posts",
  "home.all.posts": "All posts",

  // Links
  "link.home": "Home",
  "link.work": "Resume",
  "link.blog": "Blog",
  "link.projects": "Projects",

  // Footer
  "footer.terms": "Terms",
  "footer.privacy": "Privacy",
  "footer.rights": "All rights reserved",
  "footer.systems": "All systems normal",
  "footer.top": "Back to top",
};

// Add German dictionary (can be expanded later)
export const DICT_DE: Dictionary = {
  // Global
  "site.title": "Lukas Niessen",
  "site.description": "Software-Architekt und Full-Stack-Entwickler",
  "site.author": "Lukas Niessen",

  // Pages
  "work.title": "Lebenslauf",
  "work.description": "Meine berufliche Laufbahn.",
  "blog.title": "Blog",
  "blog.description": "Artikel über Themen, die mich begeistern.",
  "projects.title": "Projekte",
  "projects.description": "Aktuelle Projekte, an denen ich gearbeitet habe.",
  "search.title": "Suche",
  "search.description":
    "Durchsuche alle Beiträge und Projekte nach Stichwörtern.",

  // Work page
  "work.mode.remote": "Remote",
  "work.mode.hybrid": "Hybrid",
  "work.mode.on-site": "Vor Ort",
  "work.employmentType.full-time": "Vollzeit",
  "work.employmentType.part-time": "Teilzeit",
  "work.employmentType.contract": "Vertrag",
  "work.employmentType.freelance": "Freiberuflich",

  // Home page
  "home.subtitle": "Software-Architekt & Full-Stack-Entwickler",
  "home.about":
    "Ich bin ein Software-Architekt & Full-Stack-Entwickler mit 7 Jahren Erfahrung in Startups und Beratung. Ich leitete ein Frontend-Team und die Software-Architektur bei SocialHubs. Mein Tech-Stack umfasst: Azure, Google Cloud Platform, JavaScript, TypeScript, Angular, React, Java, Microservices und MicroFrontends. Und... ich teile gerne Wissen. 😊",
  "home.interests":
    "Ich liebe Web, Cloud, Mathematik, Klavier und Kaffee. Lass uns in Kontakt treten!",
  "home.education": "B.Sc. in Mathematik an der Universität Bonn",
  "home.connect": "Kontakt aufnehmen",
  "home.recent.projects": "Aktuelle Projekte",
  "home.all.projects": "Alle Projekte",
  "home.recent.posts": "Aktuelle Beiträge",
  "home.all.posts": "Alle Beiträge",

  // Links
  "link.home": "Startseite",
  "link.work": "Lebenslauf",
  "link.blog": "Blog",
  "link.projects": "Projekte",

  // Footer
  "footer.terms": "Nutzungsbedingungen",
  "footer.privacy": "Datenschutz",
  "footer.rights": "Alle Rechte vorbehalten",
  "footer.systems": "Alle Systeme normal",
  "footer.top": "Nach oben",
};

// Global
export const SITE: Site = {
  TITLE: DICT_EN["site.title"],
  DESCRIPTION: DICT_EN["site.description"],
  AUTHOR: DICT_EN["site.author"],
};

// Work Page
export const WORK: Page = {
  TITLE: DICT_EN["work.title"],
  DESCRIPTION: DICT_EN["work.description"],
};

// Blog Page
export const BLOG: Page = {
  TITLE: DICT_EN["blog.title"],
  DESCRIPTION: DICT_EN["blog.description"],
};

// Projects Page
export const PROJECTS: Page = {
  TITLE: DICT_EN["projects.title"],
  DESCRIPTION: DICT_EN["projects.description"],
};

// Search Page
export const SEARCH: Page = {
  TITLE: DICT_EN["search.title"],
  DESCRIPTION: DICT_EN["search.description"],
};

// Links
export const LINKS: Links = [
  {
    TEXT: DICT_EN["link.home"],
    HREF: "/",
  },
  {
    TEXT: DICT_EN["link.blog"],
    HREF: "/blog",
  },
  {
    TEXT: DICT_EN["link.work"],
    HREF: "/work",
  },
  // Projects link commented out to hide it from navigation
  // {
  //   TEXT: DICT_EN["link.projects"],
  //   HREF: "/projects",
  // },
];

// Socials
export const SOCIALS: Socials = [
  {
    NAME: "Email",
    ICON: "email",
    TEXT: "lks.niessen@gmail.com",
    HREF: "mailto:lks.niessen@gmail.com",
  },
  {
    NAME: "GitHub",
    ICON: "github",
    TEXT: "lukasniessen",
    HREF: "http://github.com/lukasniessen",
  },
  {
    NAME: "npm",
    ICON: "npm",
    TEXT: "niessen",
    HREF: "https://www.npmjs.com/~niessen",
  },
  {
    NAME: "LinkedIn",
    ICON: "linkedin",
    TEXT: "lukas-niessen",
    HREF: "http://linkedin.com/in/lukas-niessen",
  },
  {
    NAME: "X",
    ICON: "twitter-x",
    TEXT: "iamlukasniessen",
    HREF: "https://x.com/iamlukasniessen",
  },
  {
    NAME: "Medium",
    ICON: "medium",
    TEXT: "lukasniessen",
    HREF: "https://lukasniessen.medium.com/",
  },
  {
    NAME: "Dev.to",
    ICON: "dev-to",
    TEXT: "lukasniessen",
    HREF: "https://dev.to/lukasniessen",
  },
];
