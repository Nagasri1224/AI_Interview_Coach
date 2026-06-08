import "./App.css";
import { useState, useEffect,useRef } from "react";
import Webcam from "react-webcam";
function App() {

const [file, setFile] = useState(null);
const [questions, setQuestions] = useState([]);
const [currentQuestion, setCurrentQuestion] = useState(0);
const [interviewStarted, setInterviewStarted] = useState(false);
const [loading, setLoading] = useState(false);

const [transcript, setTranscript] = useState("");
const [recognition, setRecognition] = useState(null);

const webcamRef = useRef(null);



const [fillerCount, setFillerCount] = useState(0);
const [communicationScore, setCommunicationScore] = useState(0);
const [readinessScore, setReadinessScore] = useState(0);
const [status, setStatus] = useState("");
const [finalScore,setFinalScore] =useState(0);

const [eyeContactScore,
  setEyeContactScore] =
  useState(0);

const [attentionScore,
  setAttentionScore] =
  useState(0);
const [interviewData,
  setInterviewData] =
  useState([]);
const [interviewEnded,
  setInterviewEnded] =
  useState(false);

const [finalFeedback,
  setFinalFeedback] =
  useState("");
const [screen,
  setScreen] =
  useState("upload");

const uploadResume = async () => {

try {

  if (!file) {
    alert("Select Resume");
    return;
  }

  setLoading(true);

  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  const response = await fetch(
    "http://127.0.0.1:8000/upload-resume",
    {
      method: "POST",
      body: formData
    }
  );

  const data = await response.json();
  
  setQuestions(data.questions);
  

  setLoading(false);

} catch (error) {

  console.log(error);

  alert("Upload Failed");

  setLoading(false);
}

};



const generateFeedback = async () => {

try {

  const response = await fetch(
    "http://127.0.0.1:8000/feedback",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({

        question:
          questions[currentQuestion],

        answer:
          transcript
      })
    }
  );

  const data =
    await response.json();

  
  return data.feedback;

} catch (error) {

  console.log(error);

  alert(
    "Feedback Generation Failed"
  );
}

};

const analyzeAnswer = async () => {

try {

  const response = await fetch(
    "http://127.0.0.1:8000/analyze-answer",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({
        transcript: transcript
      })
    }
  );

  const data =
    await response.json();
    

  setFillerCount(
    data.filler_count
  );

  setCommunicationScore(
    data.communication_score
  );

  setReadinessScore(
    data.readiness_score
  );

  setStatus(
    data.status
  );
return data;
} catch (error) {

  console.log(error);

  alert(
    "Analysis Error"
  );
}

};
const getFinalScore = async () => {

  try {

    const response =
      await fetch(
        "http://127.0.0.1:8000/final-score",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({
            transcript
          })
        }
      );

    const data =
      await response.json();

    setFinalScore(
      data.score
    );
    console.log("Backend Final Score:", data.score);
    return data.score;

  } catch (error) {

    console.log(error);

    alert(
      "Score Calculation Error"
    );
  }
};
const downloadReport = async () => {

  try {

    const reportData = {

      final_score:
      finalScore,

      communication_score:
      communicationScore,

      readiness_score:
      readinessScore,

      status:
      status,

      filler_penalty:
      fillerCount,

      eye_contact_score:
      eyeContactScore,
      
      attention_score:
      attentionScore,

      questions:
      interviewData
    };

    console.log(
      "Sending Report:",
      reportData
    );

    const response =
      await fetch(
        "http://127.0.0.1:8000/generate-report",
        {
          method: "POST",

          headers: {
            "Content-Type":
            "application/json"
          },

          body: JSON.stringify(
            reportData
          )
        }
      );

    console.log(
      "Status:",
      response.status
    );

    if (!response.ok) {

      throw new Error(
        "Failed to generate report"
      );
    }

    const blob =
      await response.blob();

    const url =
      window.URL.createObjectURL(
        blob
      );

    const a =
      document.createElement("a");

    a.href = url;

    a.download =
      "Interview_Report.pdf";

    document.body.appendChild(
      a
    );

    a.click();

    a.remove();

  } catch (error) {

    console.log(error);

    alert(
      "Report Download Failed"
    );
  }
};

const startInterview = async () => {
  const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert(
      "Speech Recognition not supported"
    );
    return;
  }
  const recognitionInstance = new SpeechRecognition();
  recognitionInstance.continuous = true;
  recognitionInstance.interimResults = true;
  recognitionInstance.lang = "en-US";
  setRecognition(recognitionInstance);
  recognitionInstance.onresult = (event) => {
    let finalTranscript = "";
    let interimTranscript = "";
    
    for ( let i=0;
      i < event.results.length;
      i++
    ) {
      finalTranscript +=
        event.results[i][0]
          .transcript+" ";
    }
    setTranscript(finalTranscript);
  };
  recognitionInstance.start();
  alert(
    "Camera and Voice Started"
  );
  
};
const completeQuestion =
async () => {

  const feedbackText =
    await generateFeedback();

  const analysis =
    await analyzeAnswer();
    console.log("Analysis received:", analysis);
  const score =
    await getFinalScore();
    console.log("Score received:", score);
    
  const currentData = {
    
    question:
      questions[currentQuestion],

    answer:
      transcript || window.currentAnswer || "No Answer Recorded",

    feedback:
      feedbackText,

    communication_score:
      analysis.communication_score,
    readiness_score:
      analysis.readiness_score,
    status:
      analysis.status,
    final_score:
      score,

    eye_contact_score:
      eyeContactScore,

    attention_score:
      attentionScore
  };
  console.log(
    "Saving Question:",
    currentData
  );
  const updatedData = [
    ...interviewData,
    currentData
  ];
  setInterviewData(
    updatedData
  );
  console.log(
    "Updated Interview Data:",
    updatedData
  );
  return updatedData;
};
const endInterview =
async () => {
  if (recognition) {
    recognition.stop();
  }
  
  await fetch(
    "http://127.0.0.1:8000/stop-interview"
  );

  const allData = await completeQuestion();

  
  console.log(
    "All Interview Data:",
    allData
  );
  console.log(
    "All Interview Data",
    allData
  );
  const totalScore = allData.reduce(
    (sum, item) =>
      sum +
      (item.final_score || 0),
    0
  );
  const averageScore =
  allData.length >0
  ?Math.round(
    totalScore /
    allData.length
  )
  :0;

  setFinalScore(
    averageScore
  );
  
  if (
    averageScore >= 80
  ) {

    setFinalFeedback(
      "Excellent performance. You are ready for interviews."
    );

  } else if (
    averageScore >= 60
  ) {

    setFinalFeedback(
      "Good performance. Improve communication and confidence."
    );

  } else {

    setFinalFeedback(
      "Needs more practice."
    );
  }

  setInterviewStarted(false);
  setInterviewEnded(true);
  setScreen("results");
};
const nextQuestion = () => {
  if(recognition) {
    recognition.stop();
  }
  

  if (
    currentQuestion <
    questions.length - 1
  ) {
    setTranscript("");
    setCurrentQuestion(
      currentQuestion + 1
    );

    setTranscript("");
   

    setEyeContactScore(0);
    setAttentionScore(0);

    setFillerCount(0);

    setCommunicationScore(0);

    setReadinessScore(0);

    setStatus("");

    setFinalScore(0);
  }
};

return (

<div className="container">

  <h1 className="title">
    AI Interview Coach
  </h1>
  
  <input
    type="file"
    accept=".pdf"
    onChange={(e) =>
      setFile(
        e.target.files[0]
      )
    }
  />

  <br />
  <br />

  <button
  className="upload-button"
    onClick={uploadResume}
  >
    Upload Resume
  </button>

  <br />
  <br />

  {
    loading &&
    <h3>Loading...</h3>
  }

  <h2>
    Interview Questions
  </h2>

  <ul>

    {
      questions.map(
        (q, index) => (

          <li key={index}>
            {q}
          </li>
        )
      )
    }

  </ul>

  {

    questions.length > 0 && (

      <button
      className="start-button"
        onClick={() => {
          setInterviewStarted(true);
          setScreen("interview");
        }}
      >
        Start Interview
      </button>
    )
  }

  {
    screen === "interview" &&
    interviewStarted &&
    questions.length > 0 && (

      <div
        style={{
          marginTop: "30px",
          border:
            "2px solid black",
          padding: "20px"
        }}
      >

        <h2>
          Question {currentQuestion + 1}
          {" / "}
          {questions.length}
        </h2>
        <div className="webcam-container">
          <Webcam
          audio={false}
          screenshotFormat="image/jpeg"
          className="webcam"
          />
        </div>

        <p
          style={{
            fontSize: "22px",
            fontWeight: "bold"
          }}
        >
          {
            questions[
              currentQuestion
            ]
          }
        </p>
        <button
          className="btn"
          onClick={
            startInterview
          }
        >
          Start Camera & Voice
        </button>

        

        <h3>
          Transcript
        </h3>

        <p>
          {transcript}
        </p>

        

        
          {" "}
        

        {

          currentQuestion <
          questions.length - 1 && (

            <button
              className="btn"
              onClick={async () => {
                await completeQuestion();
                nextQuestion();
              }}
            >
              Next Question
            </button>
          )
        }

        

          
          <button
            className="btn"
            onClick={
              async () => {
                await endInterview();
              }
            }
          >
            End Interview
          </button>
          
        

      </div>
    )
  }

  {
    screen === "results" &&
    interviewEnded && (
      <div className="glass-card "
      >
        <h2>
          Final Interview Report
        </h2>
        <h3>
          Overall Score: {finalScore} / 100
        </h3>
        <h3>
          Final Feedback
        </h3>
        <pre
          style={{
            whiteSpace: "pre-wrap"}}
            >{finalFeedback}</pre>
            {
              interviewData.map(
                (item, index) => (
                  <div
                    key={index}
                    style={{
                      border: "1px solid gray",
                      margin: "10px",
                      padding: "10px"
                    }}
                    >
                      <h3>
                        Question {index+1}
                      </h3>
                      <p>
                        <b>Question:</b> {item.question}
                      </p>
                      <p>
                        <b>Answer:</b> {item.answer}
                      </p>
                      <p>
                        <b>Feedback:</b> {item.feedback}
                      </p>
                      <p>
                        <b>Communication:</b> {item.communication_score}
                      </p>
                      <p>
                        <b>Readiness:</b> {item.readiness_score}
                      </p>
                      <p>
                        <b>Eye Contact:</b> {item.eye_contact_score}
                      </p>
                      <p>
                        <b>Attention:</b> {item.attention_score}
                      </p>
                    </div>
                  )
                )
              }
              <button
              className="btn"
                onClick={
                  downloadReport
                }
              >
                Download PDF Report
              </button>
      </div>
    )
  }

</div>
);
}

export default App;