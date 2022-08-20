import { defineStore } from 'pinia'

export const useUserStore = defineStore({
    id: 'user',
    state()
    {
        return {
            username: "",
            session: ""
        }
    },
    actions: {
        setUsername(username: string)
        {
            this.username = username;
        },
        setSession(session: string)
        {
            this.session = session;
        }
    }
})
