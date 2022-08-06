import { Store } from "vuex"

declare module "@vue/runtime-core"
{
    interface State
    {
        username: string,
        session: string
    }

    interface ComponentCustomProperties
    {
        $store: Store<State>
    }
}