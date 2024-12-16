"use client";

import React, { useState, useEffect, useRef, useId } from "react";
import { Link } from "@nextui-org/react";
import { useOutsideClick } from "@/lib/hooks";
import { AnimatePresence, motion } from "framer-motion";
import { Videos } from "@/lib/typings";
import { decodeHtmlEntities } from "@/lib/utils";

type Props = {
  cards: Videos[];
};
// 
export default function VideoOutput({ cards }: Props) {
  const [active, setActive] = useState<(typeof cards)[number] | boolean | null>(
    null
  );
  const ref = useRef<HTMLDivElement>(null);
  const id = useId();
  const [videoSize, setVideoSize] = useState(() => {
    return { width: 0, height: 0 };
  });

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setActive(false);
      }
    }

    if (active && typeof active === "object") {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [active]);

  useOutsideClick(ref, () => setActive(null));

  useEffect(() => {
    const updateVideoSize = () => {
      if (ref.current) {
        // Get the width of the active div (70% of screen width)
        const containerWidth = window.innerWidth * 0.8;

        // Calculate height maintaining 16:9 aspect ratio
        const calculatedHeight = (containerWidth * 9) / 16;
        setVideoSize({
          width: containerWidth,
          height: calculatedHeight,
        });
      }
    };

    if (active && typeof active === "object") {
      setTimeout(updateVideoSize, 0);
    }
    window.addEventListener("resize", updateVideoSize);
    return () => window.removeEventListener("resize", updateVideoSize);
  }, [active]);

  return (
    <>
      <h2 className="mt-20 md:text-4xl text-center text-2xl">
        Watch Related Videos
      </h2>
      <p className="mb-20 text-center text-sm">
        Click on a title to watch the video
      </p>
      <AnimatePresence>
        {active && typeof active === "object" && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-transparent h-full w-full z-10"
          />
        )}
      </AnimatePresence>
      <AnimatePresence>
        {active && typeof active === "object" ? (
          <div className="fixed inset-0 grid place-items-center z-[100]">
            <motion.div
              layoutId={`card-${active.title}-${id}`}
              ref={ref}
              className="w-[80%] max-h-[85%] flex flex-col bg-white dark:bg-neutral-900 rounded-3xl overflow-hidden"
            >
              <motion.div
                layoutId={`image-${active.title}-${id}`}
                className="w-full h-full"
              >
                <iframe
                  width={videoSize.width}
                  height={videoSize.height}
                  src={`https://www.youtube.com/embed/${active.video_id}`}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  referrerPolicy="no-referrer"
                />
              </motion.div>
            </motion.div>
          </div>
        ) : null}
      </AnimatePresence>
      <ul className="max-w-[80%] mx-auto w-full gap-4">
        {cards.map((card, index) => (
          <motion.div
            layoutId={`card-${card.title}-${id}`}
            key={index}
            onClick={() => setActive(card)}
            className="p-4 flex flex-col md:flex-row justify-between items-center hover:bg-neutral-50 dark:hover:bg-neutral-800 rounded-xl cursor-pointer"
          >
            <div className="flex gap-4 flex-col md:flex-row ">
              <div className="">
                <motion.h3
                  layoutId={`title-${card.title}-${id}`}
                  className="font-medium text-neutral-800 dark:text-neutral-200 text-center md:text-left"
                >
                  {decodeHtmlEntities(card.title)}
                </motion.h3>
              </div>
            </div>
            <Link
              href={`https://youtube.com/watch?v=${card.video_id}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              <motion.button
                layoutId={`button-${card.title}-${id}`}
                className="px-4 py-2 text-sm rounded-full font-bold bg-gray-100 hover:bg-green-500 hover:text-white text-black mt-4 md:mt-0"
              >
                Visit
              </motion.button>
            </Link>
          </motion.div>
        ))}
      </ul>
    </>
  );
}

// const cards = [
//   {
//     title:
//       "Can AI predict Natural Disasters? Exploring Earthquakes, Hurricanes &amp; Floods",
//     video_id: "ogfYd705cRs",
//   },
//   {
//     title: "Mitran Di Chhatri",
//     video_id: "ogfYd705cRs",
//   },

//   {
//     title: "For Whom The Bell Tolls",
//     video_id: "ogfYd705cRs",
//   },
//   {
//     title: "Aap Ka Suroor",
//     video_id: "ogfYd705cRs",
//   },
// ];
