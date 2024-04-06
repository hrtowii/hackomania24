
export class Database {
    private data: {[key: string]: string} = {}
    private filename: string;
    constructor(filename: string) {
        Bun.file(filename).text().then((data) => {
            this.data = JSON.parse(data);
        })
        this.filename = filename;
    }
    
    push(site: string, data: string) {
        this.data[site] = data;
    }
    
    exists(site: string) {
        return this.data[site] !== undefined;
    }

    close() {
        Bun.write(this.filename, JSON.stringify(this.data));
    }
}