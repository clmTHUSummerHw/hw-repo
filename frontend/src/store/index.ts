import { createStore } from 'vuex'

interface State
{
    username: string,
    session: string
}

export default createStore<State>({
    state: {
        username: "",
        session: ""
    },

    mutations: {
        setUsername(state: State, username: string)
        {
            state.username = username;
        },

        setSession(state: State, session: string)
        {
            state.session = session;
        }
    }
})
