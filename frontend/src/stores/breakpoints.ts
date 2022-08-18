import { defineStore } from 'pinia';

export const useBreakpointsStore = defineStore({
    id: 'breakpoints',
    state()
    {
        return {
            breakpoints: new Map<string, Set<number>>()
        }
    },
    getters: {
        hasBreakpoint()
        {
            return (file: string, breakpoint: number) => {
                if(!this.breakpoints.has(file))
                    return false;

                return this.breakpoints.get(file)?.has(breakpoint);
            }
        },
        breakpointsForFile()
        {
            return (file: string) => {
                if(!this.breakpoints.has(file))
                    return new Set<number>();
                return this.breakpoints.get(file) as Set<number>;
            }
        }
    },
    actions: {
        addBreakpoint(file: string, breakpoint: number)
        {
            if(!this.breakpoints.has(file))
                this.breakpoints.set(file, new Set());

            this.breakpoints.get(file)?.add(breakpoint);
        },

        removeBreakpoint(file: string, breakpoint: number)
        {
            if(!this.breakpoints.has(file))
                return;

            if(!this.breakpoints.get(file)?.has(breakpoint))
                return;

            this.breakpoints.get(file)?.delete(breakpoint);
            if(this.breakpoints.get(file)?.size == 0)
                this.breakpoints.delete(file);
        }
    }
})
