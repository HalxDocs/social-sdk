/** Preserve integer IDs that JSON.parse would otherwise round. */
export function parseJson(text: string): unknown {
  // Match quoted strings first so digits within strings are never rewritten.
  const lossless = text.replace(
    /"(?:[^"\\]|\\[\s\S])*"|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/g,
    (token) => {
      if (token.startsWith('"') || /[.eE]/.test(token) || Number.isSafeInteger(Number(token)))
        return token;
      return `"${token}"`;
    },
  );
  return JSON.parse(lossless);
}
