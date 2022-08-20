export class FileData
{
    folder: 0 | 1 = 0
    name = ""
    files?: FileData[]
}

export default class ListFilesResult
{
    code = -1
    files: FileData[] = []
}