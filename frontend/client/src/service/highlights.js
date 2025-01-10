import axios from "axios";

const URL = import.meta.env.VITE_API_URL;

export async function getTopHighlights(data) {
    try {
        const response = await axios.post(`${URL}/list/highlights`, data, {
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 60000, // 1min
        });
        return response.data;
    }
    catch (e) {
        if (e.name == "AxiosErro") {
            return e.response.data;
        }
        console.log(e);
        return { code: -1, message: "Failed to get top highlight due to: " + e.message };
    }
}