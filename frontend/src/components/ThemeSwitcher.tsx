"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { BsMoon, BsSun } from "react-icons/bs";
import { Button } from '@nextui-org/react'

export function ThemeSwitcher() {
  const [mounted, setMounted] = useState(() => {return false})
  const { theme, setTheme } = useTheme()

  useEffect(() => {
    setMounted(true)
  }, [])

  if(!mounted) return null

  return (
    <Button
      size="sm"
      variant="ghost"
      onClick={() => setTheme(theme === "light" ? "dark" : "light")}
      className="relative w-[2rem] h-[2rem] md:w-[2.5rem] md:h-[2.5rem] 
      rounded-full flex items-center justify-center hover:scale-[1.12] 
      active:scale-105 transition-all"
    >
      {theme === "light" ? <BsMoon size={20}/> : <BsSun size={20}/>}
    </Button>
  );
};
