var threadInfoStruct = 0;
var selfThreadId = 0;
var parentThreadId = 0;
var tempDoublePtr = 0;
var STACK_BASE = 0;
var STACKTOP = 0;
var STACK_MAX = 0;
var buffer;
var DYNAMICTOP_PTR = 0;
var TOTAL_MEMORY = 0;
var STATICTOP = 0;
var staticSealed = true;
var DYNAMIC_BASE = 0;

var ENVIRONMENT_IS_PTHREAD = true;
var __performance_now_clock_drift = 0;

var Module = {};

this.addEventListener('error', function(e) {
  if (e.message.indexOf('SimulateInfiniteLoop') != -1) return e.preventDefault();

  var errorSource = ' in ' + e.filename + ':' + e.lineno + ':' + e.colno;
  console.error('Pthread ' + selfThreadId + ' uncaught exception' + (e.filename || e.lineno || e.colno ? errorSource : '') + ': ' + e.message + '. Error object:');
  console.error(e.error);
});

function threadPrint() {
  var text = Array.prototype.slice.call(arguments).join(' ');
  console.log(text);
}
function threadPrintErr() {
  var text = Array.prototype.slice.call(arguments).join(' ');
  console.error(text);
  console.error(new Error().stack);
}
function threadAlert() {
  var text = Array.prototype.slice.call(arguments).join(' ');
  postMessage({cmd: 'alert', text: text, threadId: selfThreadId});
}
out = threadPrint;
err = threadPrintErr;
this.alert = threadAlert;

Module['instantiateWasm'] = function(info, receiveInstance) {
  instance = new WebAssembly.Instance(Module['wasmModule'], info);
  delete Module['wasmModule'];
  receiveInstance(instance);
  return instance.exports;
}

this.onmessage = function(e) {
  try {
    if (e.data.cmd === 'load') {
      tempDoublePtr = e.data.tempDoublePtr;

      Module['TOTAL_MEMORY'] = TOTAL_MEMORY = e.data.TOTAL_MEMORY;
      STATICTOP = e.data.STATICTOP;
      DYNAMIC_BASE = e.data.DYNAMIC_BASE;
      DYNAMICTOP_PTR = e.data.DYNAMICTOP_PTR;

      if (e.data.wasmModule) {
        Module['wasmModule'] = e.data.wasmModule;
        Module['wasmMemory'] = e.data.wasmMemory;
        buffer = Module['wasmMemory'].buffer;
      } else {
        buffer = e.data.buffer;
      }

      PthreadWorkerInit = e.data.PthreadWorkerInit;
      if (typeof e.data.urlOrBlob === 'string') {
        importScripts(e.data.urlOrBlob);
      } else {
        var objectUrl = URL.createObjectURL(e.data.urlOrBlob);
        importScripts(objectUrl);
        URL.revokeObjectURL(objectUrl);
      }
      if (typeof FS !== 'undefined' && typeof FS.createStandardStreams === 'function') FS.createStandardStreams();
      postMessage({ cmd: 'loaded' });
    } else if (e.data.cmd === 'objectTransfer') {
      PThread.receiveObjectTransfer(e.data);
    } else if (e.data.cmd === 'run') { 
      __performance_now_clock_drift = performance.now() - e.data.time;
      threadInfoStruct = e.data.threadInfoStruct;
      __register_pthread_ptr(threadInfoStruct,0,0);
      assert(threadInfoStruct);
      selfThreadId = e.data.selfThreadId;
      parentThreadId = e.data.parentThreadId;
      assert(selfThreadId);
      assert(parentThreadId);
      STACK_BASE = STACKTOP = e.data.stackBase;
      STACK_MAX = STACK_BASE + e.data.stackSize;
      assert(STACK_BASE != 0);
      assert(STACK_MAX > STACK_BASE);
      Module['establishStackSpace'](e.data.stackBase, e.data.stackBase + e.data.stackSize);
      var result = 0;
      if (typeof writeStackCookie === 'function') writeStackCookie();
      PThread.receiveObjectTransfer(e.data);
      PThread.setThreadStatus(_pthread_self(), 1);

      try {
        result = Module['dynCall_ii'](e.data.start_routine, e.data.arg);
        if (typeof checkStackCookie === 'function') checkStackCookie();
      } catch(e) {
        if (e === 'Canceled!') {
          PThread.threadCancel();
          return;
        } else if (e === 'SimulateInfiniteLoop') {
          return;
        } else {
          Atomics.store(HEAPU32, (threadInfoStruct + 4) >> 2, (e instanceof ExitStatus) ? e.status : -2 );
          Atomics.store(HEAPU32, (threadInfoStruct + 0) >> 2, 1); 
          _emscripten_futex_wake(threadInfoStruct + 0 , 0x7FFFFFFF);
          if (!(e instanceof ExitStatus)) throw e;
        }
      }
      if (!Module['noExitRuntime']) PThread.threadExit(result);
    } else if (e.data.cmd === 'cancel') {
      if (threadInfoStruct && PThread.thisThreadCancelState == 0) {
        PThread.threadCancel();
      }
    } else if (e.data.target === 'setimmediate') {
    } else if (e.data.cmd === 'processThreadQueue') {
      if (threadInfoStruct) {
        _emscripten_current_thread_process_queued_calls();
      }
    } else {
      err('pthread-main.js received unknown command ' + e.data.cmd);
      console.error(e.data);
    }
  } catch(e) {
    console.error('pthread-main.js onmessage() captured an uncaught exception: ' + e);
    console.error(e.stack);
    throw e;
  }
}
