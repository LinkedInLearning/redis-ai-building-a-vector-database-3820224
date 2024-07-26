import fs from 'fs'
import { NextResponse } from 'next/server'
import path from 'path'

async function getData() {
  const dataDir = process.cwd() + '/app/data'
  const books = []

  try {
    const files = await fs.readdirSync(dataDir)
    for(const file of files) {
      const filePath = path.join(dataDir, file)
      const fileContent = await fs.readFileSync(filePath, 'utf8')
      const bookMetadata = extractMetadata(fileContent)

      books.push({...bookMetadata, fileName: file})
    }
    return NextResponse.json(books, {status: 200})
  } catch(error) {
    console.error(error)
    return NextResponse.json({errorMessage: error}, {status: 500})
  }
}

function extractMetadata(fileContent) {
  const titleRegex = /\s*Title:\s*(.*)/g;
  const releaseDateRegex = /\s*Release date:\s*([a-zA-Z, 0-9]+)/g;
  const authorRegex = /\s*Author:\s*(.*)/g;

  const titleMatch = fileContent.match(titleRegex)
  const title = titleMatch && titleMatch[0].replace("Title:", "").trim()

  const releaseDateMatch = fileContent.match(releaseDateRegex)
  const releaseDate = releaseDateMatch && releaseDateMatch[0].replace("Release date:", "").trim()

  const authorMatch = fileContent.match(authorRegex)
  const author = authorMatch && authorMatch[0].replace("Author:", "").trim()

  return {title, author, releaseDate}

}

export async function GET() {
  return await getData() 
}