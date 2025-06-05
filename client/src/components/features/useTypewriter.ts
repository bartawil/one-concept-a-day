import { useEffect, useState } from "react";

export default function useTypewriter(text: string, delay: number = 20) {
  const [displayedText, setDisplayedText] = useState("");

  useEffect(() => {
    if (!text) {
      setDisplayedText("");
      return;
    }

    let index = 0;
    let cancelled = false;

    const type = () => {
      if (cancelled) return;
      if (index <= text.length) {
        setDisplayedText(text.slice(0, index));
        index++;
        setTimeout(type, delay);
      }
    };

    type();

    return () => {
      cancelled = true;
    };
  }, [text, delay]);

  return displayedText;
}
