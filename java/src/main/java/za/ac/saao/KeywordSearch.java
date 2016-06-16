package za.ac.saao;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.parser.PdfReaderContentParser;
import com.itextpdf.text.pdf.parser.SimpleTextExtractionStrategy;

import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class KeywordSearch
{
    private List<String> keywords;

    // We cannot just search for the string SouthAfricanAstronomicalObservatory, as MNRAS outputs a watermark with
    // the string "South African Astronomical Observatory". We get round this issue by demanding that the string isn't
    // preceded by "at".
    private static final Pattern SAAO_PATTERN =
            Pattern.compile("(?<!at)SouthAfricanAstronomicalObservatory");

    public KeywordSearch(List<String> keywords) {
        this.keywords = keywords;
    }
    /**
     * Search for the keywords in a given PDF.
     *
     * All the keywords are searched for in the pdf, and those found are returned. White space is ignored, so for
     * example "Big Bang" is found both in the string "BigBangTheory" and the string "Big Bang Theory". The
     * keyword is found even if it is only part of a word. For example, "SHOC" is found in "a SHOCKING result".
     *
     * The order of keywords in the returned list is the same as in the original list of keywords.
     *
     * @param pdf PDF content
     * @return a list of the keywords found in the PDF
     */
    public List<String> search(InputStream pdf) throws IOException {
        PdfReader pdfReader = new PdfReader(pdf);
        PdfReaderContentParser contentParser = new PdfReaderContentParser(pdfReader);
        StringBuilder textBuilder = new StringBuilder();
        for (int i = 1; i <= pdfReader.getNumberOfPages(); i++) {
            SimpleTextExtractionStrategy strategy =
                    contentParser.processContent(i, new SimpleTextExtractionStrategy());
            textBuilder.append(strategy.getResultantText());
        }
        String text = textBuilder.toString();
        List<String> keywordsFound = new ArrayList<>();
        for (String keyword: keywords) {
            if (contains(text, keyword)) {
                keywordsFound.add(keyword);
            }
        }

        return keywordsFound;
    }

    /**
     * Checks whether a keyword is contained in some text.
     *
     * White space and hyphens are ignored in both the text and the keyword. If the keyword is "South African
     * Astronomical Observatory" it is only considered to be in the text if it isn't preceded by "at" in the text.
     * Otherwise all MNRAS articles would contain this jeyword, as they contain a watermark with it.
     *
     * @param text text
     * @param keyword keyword
     * @return whether the text contains the keyword
     */
    private static boolean contains(String text, String keyword) {
        // Look for the keyword. The keyword "South African Astronomical Observatory" needs to be handled saeparately
        // as this string is output in a watermark by MNRAS.
        text = text.replaceAll("[-\\s]", "");
        keyword = keyword.replaceAll("[-\\s]", "");
        if (!keyword.equals("SouthAfricanAstronomicalObservatory")) {
            return text.contains(keyword);
        }
        else {
            Matcher matcher = SAAO_PATTERN.matcher(text);
            return matcher.find();
        }
    }

    /**
     * Search keywords in a set of PDFs.
     *
     * The search parameters must be passed to System.in as a JSON object of the following form:
     *
     * <pre>
     *     {
     *         "pdfs": ["/path/to/file1", "/path/to/file2", ..., "/path/to/fileN"],
     *         "keywords": ["keyword1", "keyword2", ..., "keywordN"]
     *     }
     * </pre>
     *
     * The search results are output to System.out as a JSON object of the following form:
     *
     * <pre>
     * {
     *     "results": [
     *         {
     *             "pdf": "/path/to/file1",
     *             "keywords": ["keyword3", "keyword7"]
     *         },
     *         {
     *             "pdf": "/path/to/file2",
     *             "keywords": []
     *         },
     *         {
     *             "pdf": "/path/to/file3",
     *             "keywords": null
     *         }
     *     ]
     * }
     * </pre>
     *
     * {@code null} is used to indicate that the keyword search for the corresponding PDF file couldn't be executed.
     */
    public static void main(String[] argv) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        SearchParameters parameters = mapper.readValue(System.in, SearchParameters.class);

        List<SearchResult> results = new ArrayList<>();
        KeywordSearch search = new KeywordSearch(Arrays.asList(parameters.getKeywords()));
        for (String pdf: parameters.getPdfs()) {
            try {
                results.add(new SearchResult(pdf, search.search(new FileInputStream(pdf))));
            }
            catch (Exception e) {
                results.add(new SearchResult(pdf, null));
            }
        }

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        mapper.writeValue(out, Collections.singletonMap("results", results));
        System.out.println(out.toString());
    }

    private static class SearchParameters
    {
        public String[] pdfs;

        public String[] keywords;

        public String[] getPdfs()
        {
            return pdfs;
        }

        public void setPdfs(String[] pdfs)
        {
            this.pdfs = pdfs;
        }

        public String[] getKeywords()
        {
            return keywords;
        }

        public void setKeywords(String[] keywords)
        {
            this.keywords = keywords;
        }
    }

    private static class SearchResult
    {
        public String pdf;

        public String[] keywords;

        public SearchResult(String pdf, List<String> keywords) {
            this.pdf = pdf;
            if (keywords != null) {
                this.keywords = keywords.toArray(new String[] {});
            }
            else {
                this.keywords = null;
            }
        }

        public String getPdf()
        {
            return pdf;
        }

        public void setPdf(String pdf)
        {
            this.pdf = pdf;
        }

        public String[] getKeywords()
        {
            return keywords;
        }

        public void setKeywords(String[] keywords)
        {
            this.keywords = keywords;
        }
    }
}
