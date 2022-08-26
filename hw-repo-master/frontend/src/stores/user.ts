import { defineStore } from 'pinia'

class ProjectList
{
    value: string[] = []
}

export const useUserStore = defineStore({
    id: 'user',
    state()
    {
        return {
            username: "",
            session: "",
            projectList: new ProjectList()
        }
    },
    persist: {
        enabled: true
    }
})
