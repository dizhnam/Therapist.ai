import { useEffect, useState } from "react";
import { MultilineInput, TextInput, Badge } from "@canva/app-ui-kit";
import ApiCalls from "./ApiCalls";

export default function Home() {
    const [dummyUserReplies, setDummyUserReplies] = useState([
        "Hello. I am feeling depressed these days",
        "I'm worried about starting therapy. What if it doesn't help? What if I'm just beyond help?",
        // "I like red colors and blue colors",
        // "There are moments when I feel guilty for feeling this way. I have so much to be grateful for, yet I still can't shake off this sadness",
        // "Thank you for reminding me that there's hope. I'll try to hold onto that, even on the darkest days.",
        // "I want to believe that things can get better, but right now, it's hard to see a light at the end of the tunnel."
    ]);
    const [patientBackground, setPatientBackground] = useState('Summary will appear here after Document Upload.');
    const [suggestedReply, setSuggestedReply] = useState("");
    const [uploadSuccess, setUploadSuccess] = useState(false);
    const [file, setFile] = useState(null);
    const [userId, setUserId] = useState("user-111");
    const [chatHistory, setChatHistory] = useState([]);
    const [doctorChatTypeText, setDoctorChatTypeText] = useState("");
  
    useEffect(() => {
      if (file !== null) {
        handleFileSubmit();
      }
    }, [file]);
  
    const handleFileChange = (e: any) => {
        e.preventDefault();
        if (e.target.files && e.target.files.length > 0) {
            setFile(e.target.files[0]);
        }
    };
  
    const handleFileSubmit = async () => {
        if (!file) return;
        setUploadSuccess(true);
        const formData = new FormData();
        formData.append('pdfFile', file);
        let summary = await ApiCalls.startSession(userId, formData);
        setPatientBackground(summary);
    };

    const getPatientReplyBox = (name: any, reply: any) => {
        return (
            <div className="d-flex align-items-center">
                <div className="text-left pr-1"><img src="https://img.icons8.com/color/40/000000/guest-female.png" width="30" className="img1" /></div>
                <div className="pr-2 pl-1">
                <span className="name">{name}</span>
                <p className="msg">{reply}</p>
                </div>
            </div>
        )
    };

    const getDoctorReplyBox = (name: any, reply: any) => {
        return (
            <div className="d-flex align-items-center text-right justify-content-end ">
                <div className="pr-2">
                <span className="name">{name}</span>
                <p className="msg">{reply}</p>
                </div>
                <div><img src="https://i.imgur.com/HpF4BFG.jpg" width="30" className="img1" /></div>
            </div>
        )
    };

    const constructChatBox = () => {
        if(chatHistory.length === 0) {
            return <div style={{marginTop: '30%'}} className="empty-chat">
                Your chat will appear here
            </div>
        }

        return <>
            {chatHistory.map((chat: any) => {
                if(chat.party === "patient") {
                    return getPatientReplyBox("Sanjay", chat.reply);
                }
                else {
                    return getDoctorReplyBox("Dr. Hendrikson", chat.reply);
                }
            })}
        </>
    };

    const handleDoctorChatTypeText = (textContent: any) => {
        setDoctorChatTypeText(textContent);
    };

    const handleChatKeyDown = async (e: any) => {
        if(e.key === "Enter") {
            let chatHistoryNew: any = [...chatHistory];
            chatHistoryNew.push({party: "doctor", reply: doctorChatTypeText});
            setChatHistory(chatHistoryNew);
            let lastUserReply = chatHistoryNew.findLast((chat: any) => chat.party === "patient");
            ApiCalls.saveConversation(userId, (lastUserReply ? lastUserReply.reply : ""), doctorChatTypeText);
            setDoctorChatTypeText("");

            if(dummyUserReplies.length > 0) {
                setTimeout(async () => {
                    let newUserReply = dummyUserReplies[0];
                    chatHistoryNew.push({ party: "patient", reply: newUserReply });
                    setChatHistory(chatHistoryNew.slice(0));
                    setDummyUserReplies(dummyUserReplies.slice(1));
                    setSuggestedReply("...Loading...");
                    let suggestedReply = await ApiCalls.ongoingSession(userId, newUserReply);
                    setSuggestedReply(suggestedReply);
                }, 3000);
            }
        }
    };

    const handleSuggestedReplyClick = (e: any) => {
        e.preventDefault();
        setDoctorChatTypeText(suggestedReply);
    }
  
    return (   
    <div className="home-style">
      <div className="home-header">
        <h1 className="header-text">Welcome to <b>Therapist.ai</b>, your AI powered companion for counselors.</h1>
        <div className="header-upload">
            <div>
                <form onSubmit={handleFileChange}>
                    {uploadSuccess ? (
                        <img src={'./checked.png'} alt="Success" style={{ width: '70px', height: '70px' }} />
                    ) : (
                        <label htmlFor="file-upload" className="custom-file-upload">
                        <img src={'./file-upload.png'} alt="Upload" style={{ width: '70px', height: '70px' }} />
                        </label>
                    )}
                    <input id="file-upload" type="file" onChange={handleFileChange} style={{ display: 'none' }} />
                </form>
            </div>
            <p>Upload Pre-Session Questionaire</p>
        </div>
      </div>
      <div className="home-content">
        <div className="home-content-left">
            <h1 style={{ paddingTop: '20px' }}>Patient Background</h1>
            <p style={{width:'90%'}}>{patientBackground}</p>
            <h1 style={{ paddingTop: '20px' }}>Suggested Reply</h1>
            <span className="suggested-reply" onClick={handleSuggestedReplyClick}>{suggestedReply}</span>
        </div>

        <div className="home-content-right">
            <div className="home-content-right-content" style={{ width: '90%', height: '80%', paddingLeft: '20px' }}>
                <div className="d-flex justify-content-start" >
                    <div className="px-2 scroll with-padding" style={{ width: '100%', height: '100%' }}>
                        {/* {getPatientReplyBox("Sarah Anderson", "Hi Dr. Hendrikson, I haven't been feeling well for the past few days.")}
                        {getDoctorReplyBox("Dr. Hendrikson", "Let's jump on a video call")}
                        {getPatientReplyBox("Sarah Anderson", "How often should I take this?")}
                        {getDoctorReplyBox("Dr. Hendrikson", "Twice a day, at breakfast and before bed")}
                        {getPatientReplyBox("Sarah Anderson", "How often should I take this?")}
                        {getPatientReplyBox("Sarah Anderson", "Hi Dr. Hendrikson, I haven't been feeling well for the past few days.")}
                        {getDoctorReplyBox("Dr. Hendrikson", "Let's jump on a video call")}
                        {getPatientReplyBox("Sarah Anderson", "How often should I take this?")}
                        {getDoctorReplyBox("Dr. Hendrikson", "Twice a day, at breakfast and before bed")}
                        {getPatientReplyBox("Sarah Anderson", "How often should I take this?")}
                        {getPatientReplyBox("Sarah Anderson", "Hi Dr. Hendrikson, I haven't been feeling well for the past few days.")}
                        {getDoctorReplyBox("Dr. Hendrikson", "Let's jump on a video call")}
                        {getPatientReplyBox("Sarah Anderson", "How often should I take this?")}
                        {getDoctorReplyBox("Dr. Hendrikson", "Twice a day, at breakfast and before bed")}
                        {getPatientReplyBox("Sarah Anderson", "How often should I take this?")} */}
                        {constructChatBox()}
                    </div>
                </div>
                <div className="chat-input-doctor">
                    <MultilineInput
                        autoGrow
                        onChange={handleDoctorChatTypeText}
                        onKeyDown={handleChatKeyDown}
                        placeholder="Type your reply and press Enter"
                        value={doctorChatTypeText}
                    />
                </div>
            </div>
            
        </div>
      </div>
    </div>
    );
  }