declare module 'js-md5'
{
    interface Crypto
    {
        hex(): string
    }

    export function update(value: string): Crypto
}