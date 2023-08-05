using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Shoptimal
{
    public class ShopData
    {
        public HashSet<Shop> Shops { get; set; }

        public ShopData()
        {
            this.Shops = new HashSet<Shop>();
        }
    }
}
