using System.Collections.Generic;
using System.Linq;

namespace DriveHack.Site.Models
{
    public class CsvModel
    {
        public CsvModel(string name, IEnumerable<string> links)
        {
            Name = name;
            Links = links;
            MentionCount = links.Count();

        }

        public string Name;
        public int MentionCount;
        public IEnumerable<string> Links;

        public string[] ToStrings()
        {
            return new string[] { Name, MentionCount.ToString(), Links.ToString() };
        }
    }
}