import { defineStore } from 'pinia'

export const useUserStore = defineStore({
    id: 'counter',
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
