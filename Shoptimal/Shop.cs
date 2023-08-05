using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Shoptimal
{
    public class Shop
    {
        public string Name { get; set; }
        public string Location { get; set; }
        public HashSet<Item> Catalogue { get; set; }

        public Shop(string name, string location)
        {
            this.Name = name;
            this.Location = location;
            this.Catalogue = new HashSet<Item>();
        }
    }
}
