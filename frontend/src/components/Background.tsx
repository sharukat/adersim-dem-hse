"use client";
import { motion } from "framer-motion";
import React from "react";
import { AuroraBackground } from "./ui/aurora-background";
import Hero from "./Hero";

export function Background() {
  return (
    <div className="relative w-full overflow-hidden">
      <AuroraBackground className="relative">
        {/* Gradient overlay at the bottom */}
        <div className="absolute bottom-0 left-0 w-full h-40 bg-gradient-to-t from-background to-transparent" />
        
        <motion.div
          initial={{ opacity: 0.0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
            delay: 0.3,
            duration: 0.8,
            ease: "easeInOut",
          }}
          className="relative flex flex-col items-center justify-center"
        >
          <Hero />
        </motion.div>
      </AuroraBackground>
    </div>
  );
}