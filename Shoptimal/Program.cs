using System.Text.Json;

namespace Shoptimal
{
    public class Program
    {
        public static void Main()
        {
            string fileName = "ShopData.json";
            InputData.ShopDataToJSON(fileName);

            ShopData myData = InputData.JSONToShopData(fileName);
            
            Console.ReadKey();
        }
    }
}