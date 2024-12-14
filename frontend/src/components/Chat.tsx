"use client";

import { LLMInput } from "./ui/user-input";
import React, { useState, useCallback, useMemo } from "react";
import { Tabs, Tab } from "@nextui-org/tabs";
import { TextGenerateEffect } from "./ui/text-generation";
import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Button,
  Spinner,
} from "@nextui-org/react";
import { Questions, SelectedQuestion } from "@/lib/typings";
import toast, { Toaster } from "react-hot-toast";
import { useAnswerGeneration } from "@/lib/hooks";
import VideoOutput from "./Videos";


type Props = {
  Samples: Questions[];
};

export default function ChatInput({ Samples = [] }: Props) {
  const [selectedTab, setSelectedTab] = useState(() => {
    return "english";
  });
  const [userInput, setUserInput] = useState(() => {
    return "";
  });

  // Logic related to selecting a sample question
  const [isTextAnimationComplete, setIsTextAnimationComplete] = useState(() => {
    return false;
  });
  const [selectedCategory, setSelectedCategory] = useState<SelectedQuestion>(
    () => {
      return {
        categoryIndex: null,
        questionIndex: null,
      };
    }
  );

  const handleDropdownSelection = useCallback(
    (categoryIndex: number, questionIndex: number) => {
      setSelectedCategory((prev) => {
        // If clicking the same item, deselect
        if (
          prev.categoryIndex === categoryIndex &&
          prev.questionIndex === questionIndex
        ) {
          setUserInput("");
          return { categoryIndex: null, questionIndex: null };
        }

        // Select new item
        const selectedQuestion =
          Samples[categoryIndex].questions[questionIndex];
        setUserInput(selectedQuestion);
        return { categoryIndex, questionIndex };
      });
    },
    []
  );

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedCategory({ categoryIndex: null, questionIndex: null });
    setUserInput(e.target.value);
  }, []);

  const placeholders = [
    "What you want to know about AI for Disaster and Emergency management?",
    "What you want to know about AI for Human, Safety & Environment?",
  ];

  const handleTabChange = (key: React.Key) => {
    console.log("Selected Tab:", String(key));
    setSelectedTab(String(key));
  };

  const handleTextAnimationComplete = () => {
    setIsTextAnimationComplete(true);
  };

  // Activating the hooks
  const { words, isLoading, setIsLoading, generateText, setAnswerStates } =
    useAnswerGeneration(userInput, selectedTab);

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    setAnswerStates();
    setIsTextAnimationComplete(false);

    console.log("Submitting input:", userInput);

    generateText();
  };

  const memoizedDropdowns = useMemo(() => {
    return Samples?.map((sample, categoryIndex) => (
      <Dropdown
        key={categoryIndex}
        backdrop="blur"
        size="sm"
        classNames={{
          base: "min-w-[280px]",
          content: "min-w-[280px] max-h-[400px] overflow-y-auto",
        }}
      >
        <DropdownTrigger>
          <Button
            variant="flat"
            radius="full"
            className="min-w-[200px] px-auto"
          >
            {sample.category}
          </Button>
        </DropdownTrigger>
        <DropdownMenu
          variant="faded"
          aria-label="Sample Questions"
          selectionMode="single"
          selectedKeys={
            selectedCategory.categoryIndex === categoryIndex
              ? new Set([String(selectedCategory.questionIndex)])
              : new Set()
          }
          onSelectionChange={(keys) => {
            const selectedKey = Array.from(keys)[0];
            handleDropdownSelection(categoryIndex, Number(selectedKey));
          }}
          className="max-h-lg overflow-y-auto border border-transparent"
        >
          {sample.questions.map((question, questionIndex) => (
            <DropdownItem
              key={questionIndex}
              className="text-sm py-2 hover:bg-neutral-100 dark:hover:bg-neutral-800"
            >
              {question}
            </DropdownItem>
          ))}
        </DropdownMenu>
      </Dropdown>
    ));
  }, [
    Samples,
    selectedCategory.categoryIndex,
    selectedCategory.questionIndex,
    handleDropdownSelection,
  ]);

  return (
    <section key="chat" className="w-full flex flex-col items-center justify-center">
      <Toaster position="bottom-right" reverseOrder={false} />
      <div className="w-[80%] flex flex-col justify-center items-center overflow-hidden">
        <h2 className="p-4 text-xl text-center sm:text-3xl">
          Ask Me Questions
        </h2>
        <div className="px-4 flex flex-col gap-4 mb-4 items-center justify-center">
          <div className="flex flex-col items-center">
            <p className="mb-2">Choose Your Preferred Response Language:</p>
            <Tabs
              radius="full"
              color="primary"
              aria-label="Tabs colors"
              defaultSelectedKey={"english"}
              variant="bordered"
              onSelectionChange={handleTabChange}
            >
              <Tab key="english" title="English" />
              <Tab key="french" title="French" />
              <Tab key="spanish" title="Spanish" />
              <Tab key="german" title="German" />
              <Tab key="italian" title="Italian" />
            </Tabs>
          </div>

          <div className="px-4 w-full mb-4">
            <LLMInput
              externalInput={userInput}
              placeholders={placeholders}
              onChange={handleChange}
              onSubmit={onSubmit}
            />
          </div>
          <div className="flex flex-row flex-wrap items-center justify-center gap-4">
            {memoizedDropdowns}
          </div>
        </div>
        {(isLoading || words) && (
          <div className="flex flex-col gap-4 p-4">
            {isLoading ? (
              <div className="flex justify-center items-center">
                <Spinner label="Generation in Progress.." size="lg" />
              </div>
            ) : (
              <TextGenerateEffect
                words={words}
                onAnimationComplete={handleTextAnimationComplete}
              />
            )}
          </div>
        )}
      </div>

      <div className="w-[80%] flex flex-col mt-4">
        <VideoOutput />
      </div>
    </section>
  );
}
