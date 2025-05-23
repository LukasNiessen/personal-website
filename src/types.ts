export type Page = {
  TITLE: string;
  DESCRIPTION: string;
};

export interface Site extends Page {
  AUTHOR: string;
}

export type Links = {
  TEXT: string;
  HREF: string;
}[];

export type Socials = {
  NAME: string;
  ICON: string;
  TEXT: string;
  HREF: string;
}[];

export type Locale = "en" | "de";
export type Dictionary = Record<string, string>;
export type Dictionaries = Record<Locale, Dictionary>;
