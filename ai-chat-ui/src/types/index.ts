export interface CoverLetterData {
  position: string;
  companyName: string;
  aboutCompany: string;
  jobDescription: string;
}

export interface ApiResponse {
  response: string;
  error?: string;
}

export interface ICvDataResponse {
  embedded: boolean;
  message: string;
}
