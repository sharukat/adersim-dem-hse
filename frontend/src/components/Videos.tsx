"use client";

import React, { useState, useEffect, useRef, useId } from "react";
import {
  Card,
  CardFooter,
  Button,
  Link,
} from "@nextui-org/react";
import { useOutsideClick } from "@/lib/hooks";
import Image from "next/image";
import { AnimatePresence, motion } from "framer-motion";

export default function VideoOutput() {
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
      <h2 className="my-20 md:text-4xl text-center text-2xl">
        Watch Related Videos
      </h2>
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
              className="w-[80%] max-h-[80%] flex bg-white dark:bg-neutral-900 rounded-3xl overflow-hidden"
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
                />
              </motion.div>
            </motion.div>
          </div>
        ) : null}
      </AnimatePresence>
      <ul className="w-full mx-auto grid grid-cols-1 lg:grid-cols-3 2xl:grid-cols-4 items-start gap-4">
        {cards.map((card, index) => (
          <motion.div
            layoutId={`card-${card.title}-${id}`}
            key={card.title}
            onClick={() => setActive(card)}
            className="p-4 flex flex-col  hover:bg-neutral-50 dark:hover:bg-neutral-800 rounded-xl cursor-pointer"
          >
            <Card className="border-none" radius="lg">
              <Image
                alt="Woman listing to music"
                className="object-cover"
                height={300}
                src="https://nextui.org/images/hero-card.jpeg"
                width={300}
              />
              <CardFooter className="justify-between">
                <p className="text-sm">{card.title}</p>
                <Button
                  isExternal
                  className="text-sm bg-black/20"
                  color="default"
                  radius="lg"
                  size="sm"
                  as={Link}
                  variant="flat"
                  href={`https://youtube.com/watch?v=${card.video_id}`}
                >
                  Visit
                </Button>
              </CardFooter>
            </Card>
          </motion.div>
        ))}
      </ul>
    </>
  );
}

const cards = [
  {
    title: "Summertime Sadness",
    src: "https://assets.aceternity.com/demos/lana-del-rey.jpeg",
    ctaText: "Visit",
    ctaLink: "https://ui.aceternity.com/templates",
    video_id: "ogfYd705cRs",
  },
  {
    title: "Mitran Di Chhatri",
    src: "https://assets.aceternity.com/demos/babbu-maan.jpeg",
    ctaText: "Visit",
    ctaLink: "https://ui.aceternity.com/templates",
    video_id: "ogfYd705cRs",
  },

  {
    title: "For Whom The Bell Tolls",
    src: "https://assets.aceternity.com/demos/metallica.jpeg",
    ctaText: "Visit",
    ctaLink: "https://ui.aceternity.com/templates",
    video_id: "ogfYd705cRs",
  },
  {
    title: "Aap Ka Suroor",
    src: "https://assets.aceternity.com/demos/aap-ka-suroor.jpeg",
    ctaText: "Visit",
    ctaLink: "https://ui.aceternity.com/templates",
    video_id: "ogfYd705cRs",
  },
];
