package za.ac.saao;

import org.junit.Assert;
import org.junit.Test;

import java.io.InputStream;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * CUnit tests for the KeywordSearch class.
 */
public class KeywordSearchTest
{
    @Test
    public void testKeywords() throws Exception
    {
        String[] keywords = {
                "South African Astronomical Observatory",
                "SHOC",
                "Las Cumbres"
        };
        KeywordSearch search = new KeywordSearch(Arrays.asList(keywords));

        List<String> allKeywords = Arrays.asList(keywords);
        InputStream allKeywordsPdf = KeywordSearchTest.class.getResourceAsStream("data/AllKeywords.pdf");
        Assert.assertEquals(allKeywords, search.search(allKeywordsPdf));

        List<String> twoKeywords = Arrays.asList("South African Astronomical Observatory", "SHOC");
        InputStream twoKeywordsPdf = KeywordSearchTest.class.getResourceAsStream("data/TwoKeywords.pdf");
        Assert.assertEquals(twoKeywords, search.search(twoKeywordsPdf));

        List<String> noKeywords = Collections.emptyList();
        InputStream noKeywordsPdf = KeywordSearchTest.class.getResourceAsStream("data/NoKeywords.pdf");
        Assert.assertEquals(noKeywords, search.search(noKeywordsPdf));

        InputStream whiteSpaceHyphensPdf = KeywordSearchTest.class.getResourceAsStream("data/WhiteSpaceHyphens.pdf");
        Assert.assertEquals(allKeywords, search.search(whiteSpaceHyphensPdf));

        InputStream mnrasWatermarkPdf = KeywordSearchTest.class.getResourceAsStream("data/MNRASWatermark.pdf");
        Assert.assertEquals(noKeywords, search.search(mnrasWatermarkPdf));
    }
}