// app/page.tsx
import Image from "next/image";
import Hero from "@/components/Hero";
import ChatInput from "@/components/Chat";
import questionsData from '@/lib/sample_questions.json';
import { Questions } from '@/lib/typings';
import { Background } from "@/components/Background";

export default async function Home() {
  const questions: Questions[] = questionsData.all_questions;
  
  return (
    <main>
      <Background />
      <ChatInput Samples={questions}/>
    </main>
  );
}