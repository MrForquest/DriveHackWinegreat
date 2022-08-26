using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DriveHack.Site.Models;
using Microsoft.AspNetCore.Mvc;
//Собственность [Discord:@K372470#7545] запрещаю использование без запроса на согласия 

namespace DriveHack.Site.Controllers
{
    [Controller]
    public class HomeController : Controller
    {
        [Route("/")]
        public RedirectResult Default()
        {
            return Redirect("/posts");
        }

        [Route("/posts")]
        public ActionResult Index([FromServices] ApplicationContext db)
        {
            List<StartupViewItem> resultList = new List<StartupViewItem>();
            for (int id = 0; id < db.StartUp.Count(); id++)
            {
                int result = db.Props.Count(x => x.startId == id);
                resultList.Add(new StartupViewItem() { IdCount = result, Name = db.StartUp.First(x => x.id == id).name, Id = id });
            }
            return View("~/Views/Home/Index.cshtml", resultList.ToArray());
        }
        [HttpPost("/posts/withdata")]
        public ActionResult RequireTime([FromForm] RequestWithTime rq, [FromServices] ApplicationContext db)
        {
            if (rq.startTime > rq.endTime)
                return Ok();
            List<StartupViewItem> resultList = new List<StartupViewItem>();
            for (int id = 0; id < db.StartUp.Count(); id++)
            {
                int result = db.Props.Count(x => x.startId == id & x.publishTime > rq.startTime & x.publishTime < rq.endTime);
                resultList.Add(new StartupViewItem() { IdCount = result, Name = db.StartUp.First(x => x.id == id).name, Id = id });
            }
            return View("~/Views/Home/Index.cshtml", resultList.ToArray());
        }
        [HttpGet("/api/getCSV")]
        public ActionResult GetStatsFile([FromForm] RequestWithTime rq, [FromServices] ApplicationContext db)
        {
            if (rq.startTime > rq.endTime)
                return Ok();
            List<CsvModel> resultList = new();
            for (int id = 0; id < db.StartUp.Count();)
            {
                List<string> tmp = new();
                foreach (var model in db.Props.Where(x => x.startId == id & x.publishTime > rq.startTime & x.publishTime < rq.endTime).Select(x => x.link))
                    tmp.Add(model);
                resultList.Add(new CsvModel(db.StartUp.First(x => x.id == id).name, tmp.ToArray()));
            }
            StringBuilder sb = new StringBuilder();
            sb.Append("Name;Count;Links");
            foreach (var model in resultList)
            {
                sb.Append(model.Name + ';' + model.MentionCount + ',');
                foreach (var x in model.Links)
                    sb.Append(x + ',');
                sb.Append("\r\n");

            }

            return File(Encoding.UTF8.GetBytes(sb.ToString()), "text/csv", "Grid.csv");
        }

        [Route("/details")]
        public ActionResult Details(int id, [FromServices] ApplicationContext db)
        {
            var links = db.Props.Where(x => x.id == id).Select(x => x.link).AsEnumerable();
            var name = db.StartUp.First(x => x.id == id).name;
            DetailedViewItem Model = new DetailedViewItem() { Name = name, Links = links };
            return View("~/Views/Home/Details.cshtml", Model);
        }
    }

    public class RequestWithTime
    {
        public DateTime startTime;
        public DateTime endTime;
    }
}
