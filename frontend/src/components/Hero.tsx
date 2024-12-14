import React from "react"

export default function Hero() {
    return (
        <div className="w-full z-10 py-10">
            <p className="text-lg md:text-8xl font-normal py-2 text-center bg-clip-text text-transparent bg-gradient-to-b from-neutral-800 to-neutral-500 dark:from-neutral-100 dark:to-neutral-300">
                {`Artificial Intelligence`}
            </p>
            <p className="text-lg md:text-5xl font-normal py-2 text-center bg-clip-text text-transparent bg-gradient-to-b from-neutral-800 to-neutral-500 dark:from-neutral-100 dark:to-neutral-300">
                {`for`}
            </p>
            <p className="text-lg md:text-5xl font-normal py-2 text-center bg-clip-text text-transparent bg-gradient-to-b from-neutral-800 to-neutral-500 dark:from-neutral-100 dark:to-neutral-300">
                {`Disaster & Emergency Management`}
            </p>
            <p className="text-lg md:text-5xl font-normal py-2 text-center bg-clip-text text-transparent bg-gradient-to-b from-neutral-800 to-neutral-500 dark:from-neutral-100 dark:to-neutral-300">
                {`Health, Safety & Environment`}
            </p>
        </div>
    );
}