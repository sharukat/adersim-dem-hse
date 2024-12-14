export interface GeneratedResponse {
  response: string[];
}

export interface SelectedQuestion {
  categoryIndex: number | null;
  questionIndex: number | null;
}

export interface Questions{
  category: string;
  questions: string[];
};
