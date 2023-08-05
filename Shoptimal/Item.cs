using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Shoptimal
{
    public class Item
    {
        public string ItemName { get; set; }
        public float ItemPrice { get; set; }

        public Item(string itemName, float itemPrice)
        {
            this.ItemName = itemName;
            this.ItemPrice = itemPrice;
        }
    }
}
