const BASE_URL = "https://b727-146-152-226-61.ngrok-free.app";

export default {
    startSession: async (userId: any, formData: any) => {
        try {
            let url = BASE_URL + '/api/startSession/' + userId;
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });
        
            if (response.ok) {
                const data = await response.json();
                return data.summary;
            } else {
                console.error('Error uploading PDF file');
            }
        } catch (error) {
            console.error('Network error during start session:', error);
        }
        return "No summary found.";
    },
    ongoingSession: async(userId: any, userReply: any) => {
        try {
            let url = BASE_URL + '/api/ongoingSession/' + userId;
            let body = {"user_reply": userReply };
            const response = await fetch(url, {
                method: 'POST',
                body: JSON.stringify(body),
                headers: { "Content-Type": "application/json" }
            });
        
            if (response.ok) {
                const data = await response.json();
                return data.AIResponse;
            } else {
                console.error('Error uploading PDF file');
            }
        } catch(error) {
            console.error('Network error during save conversation:', error);
        }
        return "";
    },
    saveConversation: async(userId: any, userReply: any, doctorReply: any) => {
        try {
            let url = BASE_URL + '/api/saveConversation/' + userId;
            let body = {"user_reply": userReply, "counselor_reply": doctorReply };
            const response = await fetch(url, {
                method: 'POST',
                body: JSON.stringify(body),
                headers: { "Content-Type": "application/json" }
            });
        
            if (response.ok) {
                const data = await response.json();
                return data;
            } else {
                console.error('Error uploading PDF file');
            }
        } catch(error) {
            console.error('Network error during save conversation:', error);
        }
        return "";
    }
};