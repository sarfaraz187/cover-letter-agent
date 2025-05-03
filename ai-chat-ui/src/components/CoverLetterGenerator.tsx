import React, { useState, useEffect, useRef } from "react";
import { generateCoverLetter, fetchCvData } from "../services/api";
import { generateCoverLetterPDF } from "../services/pdfService";
import FormSection from "./FormSection";
import CoverLetterOutput from "./CoverLetterOutput";
import ErrorAlert from "./CvErrorAlert";
import { ICvDataResponse } from "../types/index";

const CoverLetterGenerator: React.FC = () => {
  // Form state
  const [jobDescription, setJobDescription] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [position, setPosition] = useState("");
  const [aboutCompany, setAboutCompany] = useState("");

  // Content state
  const [foundEmbeddedCv, setIsCvLoaded] = useState(false);
  const [coverLetter, setCoverLetter] = useState("");
  const [editableCoverLetter, setEditableCoverLetter] = useState("");

  // UI state
  const [isLoading, setIsLoading] = useState(false);
  const [isCvLoading, setIsCvLoading] = useState(true);
  const [error, setError] = useState("");
  const [cvError, setCvError] = useState("");
  const [copyNotification, setCopyNotification] = useState(false);
  const [downloadNotification, setDownloadNotification] = useState(false);

  // Refs
  const coverLetterRef = useRef<HTMLTextAreaElement>(null);

  // Load CV data on component mount
  useEffect(() => {
    const loadCvData = async () => {
      setIsCvLoading(true);
      setCvError("");

      try {
        const data: ICvDataResponse = await fetchCvData();
        setIsCvLoaded(data.embedded);
        console.log("CV data loaded successfully !!!!!!!!!!");
      } catch (err) {
        console.error("CV loading error:", err);
        setCvError(err instanceof Error ? err.message : "Failed to load CV data");
      } finally {
        setIsCvLoading(false);
      }
    };

    loadCvData();
  }, []);

  // Update editable cover letter when the AI generates a new one
  useEffect(() => {
    if (coverLetter) {
      setEditableCoverLetter(coverLetter);
    }
  }, [coverLetter]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!jobDescription.trim() || !position.trim() || !companyName.trim()) {
      setError("Please provide job description, position, and company name");
      return;
    }

    if (!foundEmbeddedCv) {
      setError("CV data is not available. Please refresh the page or contact support.");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      // Combine data for API request
      const formattedJobDescription = `
        Position: ${position}
        Company: ${companyName}
        About Company: ${aboutCompany}
        Job Description: ${jobDescription}
      `;

      const result = await generateCoverLetter(formattedJobDescription);
      setCoverLetter(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCoverLetterEdit = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setEditableCoverLetter(e.target.value);
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(editableCoverLetter);
    setCopyNotification(true);
    setTimeout(() => {
      setCopyNotification(false);
    }, 2000);
  };

  const handleDownloadPDF = () => {
    if (!coverLetterRef.current || !editableCoverLetter) return;

    setDownloadNotification(true);
    generateCoverLetterPDF({ position, companyName, content: editableCoverLetter });
    setTimeout(() => setDownloadNotification(false), 2000);
  };

  return (
    <div className="flex flex-col h-full max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold mb-5 text-gray-800">AI Cover Letter Generator</h1>

      <ErrorAlert error={cvError} />

      <div className="grid grid-cols-1 md:grid-cols-10 gap-6 mb-2 min-h-[600px]">
        <div className="md:col-span-4 flex flex-col">
          <FormSection
            position={position}
            companyName={companyName}
            aboutCompany={aboutCompany}
            jobDescription={jobDescription}
            error={error}
            isLoading={isLoading}
            isCvLoading={isCvLoading}
            setPosition={setPosition}
            setCompanyName={setCompanyName}
            setAboutCompany={setAboutCompany}
            setJobDescription={setJobDescription}
            onSubmit={handleSubmit}
          />
        </div>

        <div className="md:col-span-6 flex flex-col">
          <CoverLetterOutput
            coverLetter={coverLetter}
            editableCoverLetter={editableCoverLetter}
            isLoading={isLoading}
            copyNotification={copyNotification}
            downloadNotification={downloadNotification}
            coverLetterRef={coverLetterRef}
            handleCoverLetterEdit={handleCoverLetterEdit}
            handleCopyToClipboard={handleCopyToClipboard}
            handleDownloadPDF={handleDownloadPDF}
          />
        </div>
      </div>
    </div>
  );
};

export default CoverLetterGenerator;
