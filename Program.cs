using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;
using System.Linq;
using System.Net;

namespace DriveHack.Site
{
    public class Program
    {
        public static void Main(string[] args)
        {
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>

        Host.CreateDefaultBuilder(args).ConfigureWebHostDefaults(webBuilder =>
        {
            webBuilder.UseKestrel(options =>
            {
                var address = Dns.GetHostAddresses(Dns.GetHostName(), System.Net.Sockets.AddressFamily.InterNetwork).First();
                options.Listen(address, 5000);
                options.Listen(address, 5001, l =>
              {
                  l.UseHttps();
                  l.Protocols = Microsoft.AspNetCore.Server.Kestrel.Core.HttpProtocols.Http1;
              });
            });
            webBuilder.UseStaticWebAssets();
            webBuilder.UseStartup<Startup>();
        });
    }
}
