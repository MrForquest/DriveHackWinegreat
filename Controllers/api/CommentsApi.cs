using System.Security.Cryptography.X509Certificates;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using ReactExample.Models;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Text;
using System.Net.Http;

namespace ReactExample.Controllers
{
    [ApiController]
    [Route("api/comments")]
    public class CommentsApi : ControllerBase
    {
        public static List<CommentModel> _comments;

        [Route("getAll"), HttpPost]
        public JsonResult Comments([FromBody] int lastLoadId)
        {
            int count = _comments.Count;
            if (lastLoadId >= count)
                return new JsonResult (new { result = 0 });
            else
                return new JsonResult(new
                {
                    result = 1,
                    data = (_comments.Where(x => x.Id > lastLoadId - 1)).ToArray(),
                    lastId = count
                });

        }

        [Route("addComment"), HttpPost]
        public ActionResult AddComment([FromForm] CommentModel comment)
        {
            _comments.Add(comment);
            return Ok();
        }
    }
}