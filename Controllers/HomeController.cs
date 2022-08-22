using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace ReactExample.Controllers
{

    public class HomeController : Controller
    {
        [Route("/")]
        public ActionResult MainPage()
        {
            return View("~/Views/Home/MainPage.cshtml");
        }
        [Route("/authorized"), Authorize]
        public ActionResult Index()
        {
            return View("~/Views/Home/MainPage.cshtml");
        }
        [Route("/login")]
        public ActionResult Login()
        {
            return View("~/Views/Home/Login.cshtml");
        }
        [Route("/register")]
        public ActionResult Register()
        {
            return View("~/Views/Home/Register.cshtml");
        }
    }
}
