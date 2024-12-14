"use client";
import React from "react";
import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
} from "@nextui-org/react";
import { ThemeSwitcher } from "./ThemeSwitcher";

export default function Navigationbar() {
  return (
    <div className="flex justify-center w-full fixed top-0 z-20">
      <Navbar 
        maxWidth="full"
        className="w-[80%] mt-4 rounded-full bg-background/30 backdrop-blur-xl"
      >
        <NavbarContent>
          <NavbarBrand>
            <p className="font-bold text-inherit md:text-lg text-base">
              AI Assistant
            </p>
          </NavbarBrand>
        </NavbarContent>
        <NavbarContent justify="end">
          <NavbarItem>
            <ThemeSwitcher />
          </NavbarItem>
        </NavbarContent>
      </Navbar>
    </div>
  );
}