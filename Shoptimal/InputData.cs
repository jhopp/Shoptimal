using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace Shoptimal
{
    public class InputData
    {
        public static void ShopDataToJSON(string fileName)
        {
            //hardcoded example for now to show JSON formatting
            Item item1 = new Item("Bread", 0.67f);
            Item item2 = new Item("Milk", 0.74f);
            Item item3 = new Item("Cheese", 1.42f);
            Item item4 = new Item("Egg", 0.41f);

            Shop shop1 = new Shop("Lidl", "Oldstreet");
            shop1.Catalogue.Add(item1);
            shop1.Catalogue.Add(item2);

            Shop shop2 = new Shop("Aldi", "Bakerstreet");
            shop2.Catalogue.Add(item3);
            shop2.Catalogue.Add(item4);

            ShopData shopData = new ShopData();
            shopData.Shops.Add(shop1);
            shopData.Shops.Add(shop2);

            var options = new JsonSerializerOptions { WriteIndented = true };
            string jsonString = JsonSerializer.Serialize(shopData, options);
            File.WriteAllText("../../../" + fileName, jsonString);
        }

        public static ShopData JSONToShopData(string fileName)
        {
            string jsonString2 = File.ReadAllText("../../../" + fileName);
            ShopData myShop = JsonSerializer.Deserialize<ShopData>(jsonString2)!;
            return myShop;
        }
    }
}
