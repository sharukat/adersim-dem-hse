import { useState, useCallback, useEffect } from 'react';
import toast from 'react-hot-toast';

export const useAnswerGeneration = (question: string, language: string) => {
  const [words, setWords] = useState(() => {return ''});
  const [isLoading, setIsLoading] = useState(() => {return false});

  const generateText = useCallback(async () => {
    setIsLoading(true);
    setWords('');

    try {
      const response = await fetch("http://130.63.65.112:50001/generate", {
        method: "POST",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question, language: language })
      });

      const data = await response.json();
      if (data.response && data.response[0]) {
        setWords(data.response[0]);
        toast.success("Answer Generation Successful");
      } else {
        toast.error("Received invalid response format from server");
      }
    } catch (error) {
      console.error("Submission error:", error);
      toast.error("Failed to get response from server");
    } finally {
      setIsLoading(false);
    }
  }, [question, language]);

  // Reset function to clear states
  const setAnswerStates = useCallback(() => {
    setWords("");
    setIsLoading(true);
  }, []);

  return { words, isLoading, setIsLoading, generateText, setAnswerStates };
};



export const useOutsideClick = (
  ref: React.RefObject<HTMLDivElement>,
  callback: Function
) => {
  useEffect(() => {
    const listener = (event: any) => {
      if (!ref.current || ref.current.contains(event.target)) {
        return;
      }
      callback(event);
    };
 
    document.addEventListener("mousedown", listener);
    document.addEventListener("touchstart", listener);
 
    return () => {
      document.removeEventListener("mousedown", listener);
      document.removeEventListener("touchstart", listener);
    };
  }, [ref, callback]);
};