const fs = require('fs/promises');

const get_input = async (text) =>
    (await fs.readFile('day03_input.txt', 'utf-8'))
        .trim()
        .split('\n') // trim and split by lines
        // convert all to integers
        .map((line) => line.trim().split(new RegExp('[ ]+')).map(Number));

const main = async () => {
    const lines = await get_input();

    const valid_triangles = Array.from(Array(3)) // forced range (0,1,2)
        // transpose matrix, convert columns to rows
        .map((_, index) => lines.map((triangle) => triangle[index]))
        .flat() // concat rows into one dimension
        // make every 3 times into groups
        .reduce((acc, curr, idx) => {
            if (idx % 3 == 0) acc.push([curr]);
            else acc[acc.length - 1].push(curr);
            return acc;
        }, [])
        .map((sides) => sides.sort((a, b) => a - b)) // sort every group
        // filter valid triangles
        .reduce((acc, sides) => acc + (sides[0] + sides[1] > sides[2]), 0);

    return valid_triangles;
};

main().then(console.log);
