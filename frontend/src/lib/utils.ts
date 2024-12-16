import { ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}


export function decodeHtmlEntities(input: string): string {
  const parser = new DOMParser();
  const decoded = parser.parseFromString(input, "text/html").documentElement.textContent;
  return decoded || input;
}