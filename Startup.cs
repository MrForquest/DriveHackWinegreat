using JavaScriptEngineSwitcher.Extensions.MsDependencyInjection;
using JavaScriptEngineSwitcher.V8;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using React.AspNet;
using ReactExample.Controllers;
using System.Collections.Generic;
using ReactExample.Models;
using Microsoft.AspNetCore.Identity;

namespace ReactExample
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        public void ConfigureServices(IServiceCollection services)
        {

            services.AddControllersWithViews(x => x.EnableEndpointRouting = false);
            services.AddSingleton<IHttpContextAccessor, HttpContextAccessor>();
            services.AddReact();
            services.AddDbContext<AuthorizationContext>();
            services.AddIdentity<AuthorizationUser, IdentityRole>()
                .AddEntityFrameworkStores<AuthorizationContext>();
            services.AddCors();
            services.AddJsEngineSwitcher(options => options.DefaultEngineName = V8JsEngine.EngineName).AddV8();
        }

        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            app.UseHttpsRedirection();
            app.UseReact(config =>
            {
                config.AddScriptWithoutTransform("~/js/remarkable.min.js");
                config.AddScript("~/js/realtimeClock.jsx");
                config.AddScript("~/js/commentBox.jsx");
                config.AddScript("~/js/authorizedCommentBox.jsx");

            });
            app.UseAuthentication();
            app.UseAuthorization();
            app.UseCors(x =>
            {
                x.AllowAnyHeader();
                x.AllowAnyMethod();
            });
            app.UseStaticFiles();
            app.UseMvc();
            CommentsApi._comments = new List<CommentModel>();
            CommentsApi._comments.Add(new CommentModel { Id = 0, Author = "Хороший челик", Text = "Это первое тестовое сообщение" });
        }
    }
}
