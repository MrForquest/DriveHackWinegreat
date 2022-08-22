using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using ReactExample.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ReactExample.Controllers.api
{
    [ApiController]
    public class AuthorizationApi : ControllerBase
    {
        private readonly UserManager<AuthorizationUser> userManager;
        private readonly SignInManager<AuthorizationUser> loginManager;

        public AuthorizationApi(UserManager<AuthorizationUser> userManager, SignInManager<AuthorizationUser> signInManager)
        {
            this.loginManager = signInManager;
            this.userManager = userManager;
        }

        [HttpPost]
        public async Task<IActionResult> Register(UserModel model)
        {
            AuthorizationUser user = new AuthorizationUser { UserName = model.UserName };
            var result = await userManager.CreateAsync(user, model.Password);
            if (result.Succeeded)
            {
                await loginManager.SignInAsync(user, false);
                return RedirectToAction("Index", "Home");
            }
            else
            {
                return ValidationProblem();
            }
        }
        [HttpPost]
        public async Task<IActionResult> Login(UserModel model)
        {
            var result = await loginManager.PasswordSignInAsync(model.UserName, model.Password, false, false);
            if (result.Succeeded)
            {
                return Ok();
            }
            return ValidationProblem();
        }
    }
}
